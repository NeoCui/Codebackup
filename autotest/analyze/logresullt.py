#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 17, 2018
logresult.py: Get the log analyze report. 
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

#check if the input is right
def check(var_sysosid, session):
	flag = session.query(SQLClass.system_os).filter(SQLClass.system_os.system_osid == var_sysosid).first()
	if flag:
		return flag.system_osid
	else:
		return -1

#get the analyzed pci information in the database
def getresult(var_sysosid, session):
	count = 0
	#Clear the logresult table
	try:
		session.query(SQLClass.logresult).delete()
		session.commit()
	except Exception as e:
		session.rollback()
		autotestlog.logger.error(e.message)
	#Get the right os based drivers
	logs = session.query(SQLClass.log_system_os).filter(SQLClass.log_system_os.systemosid==var_sysosid).all()
	logfileobj = session.query(SQLClass.system_os).filter(SQLClass.system_os.system_osid==var_sysosid).first()
	
	#Get the log information 
	for item in logs:
		count += 1
		status = model.stsEnum.invalid
		tmp = session.query(SQLClass.log).filter(and_(SQLClass.log.logid == item.logid,SQLClass.log.status != status)).first()
		row = SQLClass.logresult(no=count,information=tmp.information,error_type=tmp.error_type,source=tmp.source, \
				linenumber=tmp.linenumber,logfile=logfileobj.logfile, bznumber = item.bznumber)
		try:
			session.add(row)
			session.commit()
		except Exception as e:
			session.rollback()
			if e.message.find("Duplicate entry") < 0:
				autotestlog.logger.error(e.message)
#
#dump pciresult table information to excel
	result = session.query(SQLClass.logresult).all()
	key, data = toexcel.query_log(result)
	df = pd.DataFrame(data, columns=key)
	df = df[['no', 'information', 'error_type', 'source', 'logfile']]
	filename = logfileobj.logfile + 'logresult.xls'
	df.to_excel(filename, index=False)

#print help information
def usage():
	print "usage: {0} [OPTS]".format(os.path.basename(__file__))
	print "  -i, --id <system_os id>	Output the pciid result for the specified system_os id"
	print "  -h, --help					Print this help message"
	
def main(argv):
	if argv:
		try:
			opts, args = getopt.getopt(argv, "hvi:", ["system_osid="])
		except getopt.GetoptError as err:
			print str(err)
			sys.exit(2)
		var_sysosid = None
		verbose = False
		for opt, arg in opts:
			if opt == '-v':
				verbose = True
			elif opt in ("-i", "--system_osid"):
				var_sysosid = arg
				return var_sysosid
			elif opt in ("-h", "--help"):
				usage()
				sys.exit()
			else:
				assert False, "unhandled option"
	else:
		usage()
		sys.exit(2)

#logAnalyze()
def logAnalyze():
	ret = main(sys.argv[1:])
	if ret:
		#connect to the database
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
			getresult(flag, session)
		else:
			print "Please input the right parameter!"
		session.close()
		engine.dispose()
	else:
		print "Error input parameter!"
		usage()
		sys.exit(2)

if __name__ == '__main__':
	logAnalyze()
