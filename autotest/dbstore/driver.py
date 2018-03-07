#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 09, 2018
driver.py: handle the driver information under /home/information/drivers/OSVs/version/**.txt
@author: Neo
'''
import sys, os, md5, getopt
sys.path.append("/root/Project/autotest")
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlserver import SQLClass
from common import rdgenerator, autotestlog, model

#global variables
imgname = ''
osname = ''
osversion = ''
osdict = {'RedHat': 'Red Hat Enterprise Linux Server', 'SUSE': 'SUSE Enterprise Linux Server'}

# 递归遍历指定目录，显示目录下的所有文件名
def allFiles(rootdir, session):
    global imgname
    iso = 'iso.txt'
    list_dirs = os.walk(rootdir)
    for root, dirs, files in list_dirs:
		for f in files:
			filename = os.path.join(root, f)
			if f[-7:] == iso:
				#print "filename is: ", f
				nPos = f.index(iso)
				rd = rdgenerator.id_generator()
				imgname = f[0:-4]
				newname = f[0:nPos+4] + rd
				print "newname: ", newname
				driverHandle(filename, session)
				os.rename(filename, os.path.join(root, newname))

#handle pciid file
def driverHandle(filename, session):
    extko = "===>ko"
    extpci = "===>pciid"
    extinfo = "===>modinfo"
    extrpm = "===>rpm"
    extname = "/"
    extsrcver = "srcversion"
    extver = "version"
    extlib = "lib"
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    nPos = 0
    koflag = False
    pciflag = False
    infoflag = False
    rpmflag = False
    count = 0
    global osdict, imgname, osname, osversion
    var_osid = ''
    var_drvid = ''
	#driver dictionary
    driver = {'name': '', 'version': '', 'srcversion': '', 'vd': '', \
			'svsd': '', 'location': '', 'rpmlocation': '', 'modinfo': ''}
    flag = session.query(SQLClass.os).filter(SQLClass.os.imgname == imgname).first()
    if flag:
		var_osid = flag.osid
    else:
		ositem = SQLClass.os(name=osdict[osname], platform='x86_64', version=osversion, imgname=imgname) 
		try:
			session.add(ositem)
			session.flush()
			print "Add the [%s %s] into the database!" % osdict[osname],osversion
			var_osid = ositem.osid
			session.commit()
		except Exception as e:
			session.rollback()
			if e.message.find("Duplicate entry") < 0:
				autotestlog.logger.error("Update driver table failed with no OS item found in the OS table")
				return -1
	
    for eachLine in lines:
		eachLine= eachLine.strip('\n')
#		print eachLine
		if eachLine.find(extko) >= 0:
		#    print eachLine
		    count += 1
		    koflag = True
		    rpmflag = False
		    continue
		elif eachLine.find(extpci) >= 0:
#		    print eachLine
		    pciflag = True
		    continue
		elif eachLine.find(extinfo) >= 0:
#		    print eachLine
		    infoflag = True
		    pciflag = False
		    continue
		elif eachLine.find(extrpm) >= 0:
			rpmflag = True
			infoflag = False
			continue
		elif koflag:
#		    print eachLine
			if count ==2 : 
				mdobj = md5.new()
				mdobj.update(driver['vd'])
				mdobj = mdobj.hexdigest() 
				flag = session.query(SQLClass.driver).filter(and_(SQLClass.driver.md5 == mdobj, \
					SQLClass.driver.name == driver['name'], SQLClass.driver.srcversion == driver['srcversion'])).first()	
				if flag:
					print "Already exists", flag.driverid
					var_drvid = flag.driverid
				else:
					driveritem = SQLClass.driver(name=driver['name'], version=driver['version'], \
						vd=driver['vd'], svsd=driver['svsd'], location=driver['location'], \
						rpmlocation=driver['rpmlocation'], modinfo=driver['modinfo'], \
						srcversion=driver['srcversion'], md5=mdobj, osid=var_osid)
					try:
						session.add(driveritem)
						session.flush()
						print "driver id is:", driveritem.driverid
						var_drvid = driveritem.driverid
						session.commit()
					except Exception as e:
						session.rollback()
						if e.message.find("Duplicate entry") < 0:
							autotestlog.logger.error(e.message)
				driver['version'] = ''
				driver['vd'] = ''
				driver['svsd'] = ''
				driver['srcversion'] = ''
				driver['modinfo'] = ''
				var_drvid = ''
				count = 1
			nPos = eachLine.rfind(extname)
			mPos = eachLine.find(extlib)
			driver['name'] = eachLine[nPos+1:]
			driver['location'] = eachLine[mPos:]
			koflag = False
		elif pciflag:
#		    print eachLine
			data = eachLine.split("::")
			if data[0] != '*:*':
				driver['vd'] = driver['vd'] + data[0] + '\n'
			driver['svsd'] = driver['svsd'] + data[1] + '\n'
		elif infoflag:
#		    print eachLine
			if eachLine[0:10] == extsrcver:
			    nPos = eachLine.find(extsrcver)
			    driver['srcversion'] = eachLine[nPos+16:] 
			if eachLine[0:7] == extver:
			    nPos = eachLine.find(extver)
			    driver['version'] = eachLine[nPos+16:]
			driver['modinfo'] = driver['modinfo'] + eachLine + '\n'
		elif rpmflag:
			driver['rpmpackage'] = eachLine
		else:
#		    print eachLine
		    print "Error: should check your condition"
    mdobj = md5.new()
    mdobj.update(driver['vd'])
    mdobj = mdobj.hexdigest()
    flag = session.query(SQLClass.driver).filter(and_(SQLClass.driver.md5 == mdobj, \
			SQLClass.driver.name == driver['name'], SQLClass.driver.srcversion == driver['srcversion'])).first()	
    if flag:
		print "Already exists"
		var_drvid = flag.driverid
    else:
		driveritem = SQLClass.driver(name=driver['name'], version=driver['version'], \
			vd=driver['vd'], svsd=driver['svsd'], location=driver['location'], \
			rpmlocation=driver['rpmlocation'], modinfo=driver['modinfo'], \
			srcversion=driver['srcversion'], md5=mdobj, osid=var_osid)
		try:
			session.add(driveritem)
			session.flush()
			print "driver id is:", driveritem.driverid
			var_drvid = driveritem.driverid
			session.commit()
		except Exception as e:
			session.rollback()
			if e.message.find("Duplicate entry") < 0:
				autotestlog.logger.error(e.message)
    fopen.close()

#print help information
def usage():
	print "usage: {0} [OPTS]".format(os.path.basename(__file__))
	print "  -d, --directory <driver information directory>	Store the driver information in the database"
	print "  -h, --help										Print this help message"
#read arguments
def main(argv):
	if argv:
		try:
			opts, args = getopt.getopt(argv, "hvd:", ["directory="])
		except getopt.GetoptError as err:
			print str(err) 
			sys.exit(2)
		drv_dir = None
		verbose = False
		for opt, arg in opts:
			print opt, arg
			if opt == '-v':
				verbose = True
			elif opt in ("-d", "--directory"):
				drv_dir = arg
				return drv_dir
			elif opt in ("-h", "--help"):
				usage()
				sys.exit()
			else:
				assert False, "unhandled option"
	else:
		usage()
		sys.exit(2)
#driverDB()
def driverDB(param):
	global osname, osversion
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
	sPos = model.findSubstring(param, '/', 1)
	osname = param[:sPos]
	osversion = param[sPos+1:]
	rootdir= "/home/information/drivers/" + param
	allFiles(rootdir, session)
	session.close()
	engine.dispose()


if __name__ == '__main__':
	ret = main(sys.argv[1:])
	if ret:
		driverDB(ret)
	else:
		print "Error input parameter!"
		usage()
		sys.exit(2)
