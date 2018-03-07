#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb 01, 2018
report.py: Get the testing report. 
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

#check if the input is right and the system_os exists
def check(var_sysosid, session):
	flag = session.query(SQLClass.system_os).filter(SQLClass.system_os.system_osid == var_sysosid).first()
	if flag:
		return flag.system_osid
	else:
		return -1

#get the analyzed pci information in the database
def getresult(var_sysosid, session):
	report = {'sysconfig':'', 'tcname':'','status':''}
	configuration = []
	count = 0
	#Clear the logresult table
	try:
		session.query(SQLClass.report).delete()
		session.commit()
	except Exception as e:
		session.rollback()
		autotestlog.logger.error(e.message)
	#Get the right system os information
	sysos_obj = session.query(SQLClass.system_os).filter(SQLClass.system_os.system_osid==var_sysosid).first()
	sys_obj = session.query(SQLClass.system).filter(SQLClass.system.systemid==sysos_obj.systemid).first()
	os_obj = session.query(SQLClass.os).filter(SQLClass.os.osid==sysos_obj.osid).first()
	#bios mode
	configuration.append('BIOS mode:') 
	configuration.append(sys_obj.biosmode) 
	configuration.append('\n') 
	#platform
	configuration.append('Platform:') 
	configuration.append(sys_obj.model) 
	configuration.append('\n') 
	#processor
	configuration.append('Processor:') 
	configuration.append(sys_obj.processor) 
	configuration.append('\n') 
	#os information
	configuration.append('Operating System:') 
	configuration.append(os_obj.name) 
	configuration.append(os_obj.version) 
	configuration.append('\n') 
	report['sysconfig'] = ' '.join(configuration)
	
	#Get the testcase status
	tcresult_path = sysos_obj.logfile + 'report.txt'
	fopen = open(tcresult_path, 'r')
	lines = fopen.readlines()
	for line in lines:
		count += 1
		info = line.split(' ')
		report['tcname'] = info[1]
		report['status'] = info[2] 
		row = SQLClass.report(no=count,tcname=report['tcname'], \
				status=report['status'])
		try:
			session.add(row)
			session.commit()
		except Exception as e:
			session.rollback()
			autotestlog.logger.error(e.message)
#
#dump pciresult table information to excel
	config_df = pd.DataFrame(data={'System Configuration':report['sysconfig']})
	result = session.query(SQLClass.report).all()
	key, data = toexcel.query_to_list(result)
	result_df = pd.DataFrame(data, columns=key)
	result_df = df[['no', 'tcname', 'status']]
	filename = sysos_obj.logfile + 'report.xls'
	config_df.to_excel(filename, sheetname = 'system config', index=False)
	result_df.to_excel(filename, sheetname = 'test result', index=False)

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

#Report()
def testReport():
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
	testReport()
