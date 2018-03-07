#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 13, 2018
initHandle.py: check the file under status and get the system, os information 
check the file under status folder. The filename is init_time_system_osnameosversion
The image name is in the file.
Change the file name to done_time_system_osnameosversion when completing operation.
@author: Neo
'''
import sys, os, re
sys.path.append("/root/Project/autotest")
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlserver import SQLClass
from common import rdgenerator, autotestlog, model

#global variables
osname = ""
osversion = ""
logparam = {'sysosid': '', 'logdir': ''}
param = {'model': '', 'imgname': '', 'processor': ''}
osdict = {'RedHat': 'Red Hat Enterprise Linux Server', 'SUSE': 'SUSE Enterprise Linux Server', \
		'test': 'testing OS'}

# 递归遍历指定目录，显示目录下的所有文件名
def allFiles(rootdir):
    global osname, osversion, param 
    extso = '_'
    list_dirs = os.walk(rootdir)
    for root, dirs, files in list_dirs:
		##get the system and osname
		for f in files:
			if f.find('.txt') > 0:
				filename = os.path.join(root, f)
				print filename
				sPos = model.findSubstring(f, extso, 3)
				ePos = model.findSubstring(f, extso, 4)
				osname = f[sPos+1:ePos]
				osname = osdict[osname]
				sPos = f.find('.txt')
				osversion = f[ePos+1:sPos]
				sPos = model.findSubstring(f, extso,2)
				ePos = model.findSubstring(f, extso,3)
				param['model'] = f[sPos+1:ePos]
				print "filename:", filename
				print "model: ", param['model']
				print "osname: ", osname 
				print "osversion: ", osversion 
				logparam['logdir'] = osname + "/" + osversion
				imgnameHandle(filename)
				print "image name: ", param['imgname'] 
				print "processor:", param['processor']
				rd = rdgenerator.id_generator()
				newname = f[0:-3]+rd
				os.rename(filename, os.path.join(root,newname))
				#os.remove(filename)
			else:
				pass	

#handle SUSE log file - messages
def imgnameHandle(filename):
    global param 
    fopen = open(filename, 'r')
    data = fopen.readlines()
    for x in data:
		x = x.strip('\n')
		if x.find('ersion') >= 0:
			param['processor'] = x[8:]
		elif x.find("iso") > 0:
		    param['imgname'] = x
    fopen.close()

#update the system, os information in the database
def updatedb(session):
	global osname, osversion, param
	var_osid = ''
	var_sysid = ''
	if re.match('rd', param['model']) or re.match('td', param['model']) or re.match('rs', param['model']) \
			or re.match('ts', param['model']) or re.match('rq', param['model']):
		serie = 'thinkserver'
	elif re.match('x', param['model']):
		serie = 'thinksytem'
	elif re.match('sr', param['model']) or re.match('st', param['model']):
		serie = 'thinksystem'
	else:
		print "No matched series found!"
	#check if os already added in the database
	flag = session.query(SQLClass.os).filter(SQLClass.os.imgname == param['imgname']).first()
	if flag:
		print "Already exists!"
		print "osid is:", flag.osid
		var_osid = flag.osid
	else:
		ositem = SQLClass.os(name=osname, platform ='x86_64', version=osversion, imgname=param['imgname'])
		try:
			session.add(ositem)
			session.flush()
			print "osid is:", ositem.osid
			var_osid = ositem.osid
			session.commit()
		except Exception as e:
			session.rollback()
			if e.message.find("Duplicate entry") < 0:
				autotestlog.logger.error(e.message)
	#check if system already added in the database
	flag = session.query(SQLClass.system).filter(and_(SQLClass.system.model == param['model'], \
			SQLClass.system.processor == param['processor'])).first()
	if flag:
		print "Already exists!"
		print "system id is:", flag.systemid
		var_sysid = flag.systemid
	else:
		sysitem = SQLClass.system(series=serie, model=param['model'], processor=param['processor'])
		try:
			session.add(sysitem)
			session.flush()
			print "system id is:", sysitem.systemid
			var_sysid = sysitem.systemid
			session.commit()
		except Exception as e:
			session.rollback()
			if e.message.find("Duplicate entry") < 0:
				autotestlog.logger.error(e.message)
	if var_osid and var_sysid:
		flag = session.query(SQLClass.system_os).filter(and_(SQLClass.system_os.systemid \
				== var_sysid, SQLClass.system_os.osid == var_osid)).first()
		if flag:
			print "Already exits!"
			print "system_os id is:", flag.system_osid
			logparam['sysosid'] = flag.system_osid
		else:
			sysositem = SQLClass.system_os(systemid=var_sysid, osid=var_osid)
			try:
				session.add(sysositem)
				session.flush()
				print "system_os id is:", sysositem.system_osid
				logparam['sysosid'] = sysositem.system_osid
				session.commit()
			except Exception as e:
				session.rollback()
				if e.message.find("Duplicate entry") < 0:
					autotestlog.logger.error(e.message)

#initDB()
def initDB(rootdir):
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
	print "Searching file change...."
	ret = allFiles(rootdir)
	if ret == 0:
		print "Updating system and os table"
		updatedb(session)
	print "Done."
	session.close()
	engine.dispose()
	return logparam


if __name__ == '__main__':
	rootdir= "/home/information/status"
	initDB(rootdir)
