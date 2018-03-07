#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 17, 2018
pciresult.py: Get the pciid analyzing report. 
@author: Neo
'''
import os, sys, getopt
import pandas as pd
sys.path.append("/root/Project/autotest")
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlserver import SQLClass
from common import autotestlog, toexcel, model

#global variable
osdict = {'Red Hat Enterprise Linux Server': 'RedHat', 'SUSE Enterprise Linux Server': 'SUSE'}

#check if the input is right
def check(var_imgname, session):
	flag = session.query(SQLClass.os).filter(SQLClass.os.imgname == var_imgname).first()
	if flag:
		return flag.osid
	else:
		return -1

#get the analyzed pci information in the database
def getresult(var_osid, ret, session):
	count = 0
	#Clear the pciresult table
	try:
		session.query(SQLClass.pciresult).delete()
		session.commit()
	except Exception as e:
		session.rollback()
		autotestlog.logger.error(e.message)
	#Get the righ os based drivers
	os = session.query(SQLClass.os).filter(SQLClass.os.osid==var_osid).first()
	osname = osdict[os.name]
	osversion = os.version
	
	#Get the pciid from BB team
	devices = session.query(SQLClass.pciid).filter(SQLClass.pciid.status == '1').all()
	for device in devices:
		count += 1
		isexist = model.estEnum.NA
		drvname = ''
		drvver = ''
		pciid = device.vendorid + ':' + device.deviceid
		pciidu = pciid.upper()
		pciidl = pciid.lower()
		#check if the device is supported in specific OS
		drvinfo = session.query(SQLClass.driver).filter(and_(or_(SQLClass.driver.vd.contains(pciidu), \
				SQLClass.driver.vd.contains(pciidl)), SQLClass.driver.osid == var_osid)).first()
		if drvinfo:
			isexist = model.estEnum.exist
			drvname = drvinfo.location
			drvver = drvinfo.version
		row = SQLClass.pciresult(no=count,vendor=device.vendor,description=device.description,vendordevice=pciid, \
				project=device.project,exists=isexist,drivername=drvname,driverversion=drvver)
		try:
			session.add(row)
			session.commit()
		except Exception as e:
			session.rollback()
			if e.message.find("Duplicate entry") < 0:
				autotestlog.logger.error(e.message)

    #dump pciresult table information to excel
	result = session.query(SQLClass.pciresult).all()
	key, data = toexcel.query_pci(result)
	df = pd.DataFrame(data, columns=key)
	#change order
	df = df[['no','vendor','description','vendordevice','drivername','driverversion','project','exists']]
	filename = '/home/information/drivers/' + osname + '/' + osversion + '/' + ret[0:-3] + 'xls'
	df.to_excel(filename, index=False)

#print help information
def usage():
	print "usage: {0} [OPTS]".format(os.path.basename(__file__))
	print "  -i, --imgname <OS image name>		Output the pciid result for the specified OS"
	print "  -h, --help							print this help message"

#handle input parameter
def main(argv):
	#outputfile = ''
	if argv:
		try:
			opts, _ = getopt.getopt(argv, 'hvi:', ['help', 'verbose', 'imgname='])
		except getopt.GetoptError as err:
			print str(err) 
			sys.exit(2)
		var_imgname = None 
		verbose = False
		for opt, arg in opts:
			if opt == '-v':
				verbose = True
			elif opt in ("-i", "--imgname"):
				var_imgname = arg
				return var_imgname
			elif opt in ("-h", "--help"):
				usage()
				sys.exit()
			else:
				assert False, "unhandled option"
	else:
		usage()
		sys.exit(2)

#pciAnalyze()
def pciAnalyze():
	ret = main(sys.argv[1:])
	if ret:
		engine = model.connectDB()
		print "Create database session..."
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		print "Done."
		print "Create metadata object..."
		meta = MetaData(bind=engine)
		meta.reflect(bind=engine)
		model.Base.metadata.create_all(engine, checkfirst=True)
		print "Done."
		flag = check(ret, session)
		if flag != -1:
			getresult(flag, ret, session)
		else:
			print "Please input the right OS image name!"
		session.close()
		engine.dispose()
	else:
		print "Error input parameter"
		usage()
		sys.exit(2)

if __name__ == '__main__':
	pciAnalyze()
