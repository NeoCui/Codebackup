#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Dec 27, 2017
SQLClass.py: mysql database operational class using sqlalchemy
@author: Neo
'''
import sys, enum
sys.path.append("/root/Project/autotest")
from sqlalchemy import * 
from sqlalchemy.orm import *
from common import model
from datetime import datetime


class user(model.Base):
	__tablename__ = 'User'
	__table_args__ = (Index('unique_constratint', "username", unique=True),)
	userid = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
	firstname = Column(String(16), nullable=False)
	lastname = Column(String(16), nullable=False)
	username = Column(String(64), nullable=False)
	password = Column(String(64), nullable=False)

class log_system_os(model.Base):
	__tablename__ = 'log_system_os'
	__table_args__ = (Index('unique_constraint', "logid", "systemosid", unique=True),)
	log_osid = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
	logid = Column(Integer, ForeignKey('log_table.logid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
	systemosid = Column(Integer, ForeignKey('system_os.system_osid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
	bznumber = Column(Integer)
	rs_systemos = relationship('system_os', back_populates='logs')
	rs_log = relationship('log', back_populates='sysoses') 

class log(model.Base):
	__tablename__ = 'log_table'
	__table_args__ = (Index('unique_constraint', "md5", unique=True),)
	logid = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
	information = Column(BLOB, nullable=False)
	error_type = Column(Enum(model.typEnum), default=model.typEnum.error)
	source = Column(Enum(model.srcEnum), default=model.srcEnum.dmesg)
	status = Column(Enum(model.stsEnum), default=model.stsEnum.valid)
	comment = Column(BLOB)
	md5 = Column(String(64), nullable=False, unique=True)
	sysoses = relationship('log_system_os', back_populates='rs_log')

class system_os(model.Base):
	__tablename__ = 'system_os'
	__table_args__ = (Index('unique_constraint', "systemid", "osid", unique=True),)
	system_osid = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
	systemid = Column(Integer, ForeignKey('system_table.systemid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
	osid = Column(Integer, ForeignKey('os_table.osid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
	logfile = Column(String(60), nullable=False)
	logs = relationship('log_system_os', back_populates='rs_systemos')
	rs_system = relationship('system', back_populates='os2')
	rs_os2 = relationship('os', back_populates='systems')

#os_table object:
class os(model.Base):
	#table name:
	__tablename__ = 'os_table'
	__table_args__ = (Index('unique_constraint', "imgname", unique=True),)
	#table structure:
	osid = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
	name = Column(String(60), nullable=False)
	version = Column(String(45), nullable=False)
	imgname = Column(String(60), nullable=False)
	phase = Column(String(45))
	platform = Column(Enum(model.plmEnum), default=model.plmEnum.x86_64)
	drivers = relationship('driver', back_populates='os')
	systems = relationship('system_os', back_populates='rs_os2')

class driver(model.Base):
	__tablename__ = 'driver_table'
	__table_args__ = (Index('unique_constraint', "name", "version", "location", "md5", unique=True),)
	driverid = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
	name = Column(String(60), nullable=False)
	srcversion = Column(String(20), nullable=False)
	version = Column(String(60), nullable=False)
	vd = Column(Text, nullable=False)
	svsd = Column(Text)
	location = Column(String(160), nullable=False)
	rpmlocation = Column(String(160), nullable=False)
	modinfo = Column(BLOB, nullable=False)
	md5 = Column(String(64), nullable=False)
	osid = Column(Integer, ForeignKey('os_table.osid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
	os = relationship('os', back_populates='drivers')
	
class system(model.Base):
	__tablename__ = 'system_table'
	__table_args__ = (Index('unique_constraint', "model", "processor", unique=True),)
	systemid = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
	series = Column(Enum(model.srsEnum), default=model.srsEnum.thinksystem)
	biosmode = Column(Enum(model.modEnum), default=model.modEnum.UEFI)
	codename = Column(String(30), ForeignKey('codename_table.codename', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
	model = Column(String(80), nullable=False)
	processor = Column(String(80), nullable=False)
	os2 = relationship('system_os', back_populates='rs_system')
	rs_cdnm = relationship('codename', back_populates='rs_sys')

class codename(model.Base):
	__tablename__ = 'codename_table'
	__table_args__ = (Index('unique_constraint', "codename", unique=True),)
	cnmid = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
	codename = Column(String(30), nullable=False)
	model = Column(String(80), nullable=False)
	description = Column(String(255), nullable=True)
	SS = Column(Date, nullable=False)
	rs_sys = relationship('system', back_populates='rs_cdnm')	

class pciid(model.Base):
	__tablename__ = 'pciid_table'
	__table_args__ = (Index('unique_constraint', "description", "vendorid", "deviceid", "subvendorid", "subdeviceid", unique=True),)
	pciidid = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
	vendor = Column(String(45), nullable=False)
	description = Column(String(160), nullable=False)
	vendorid = Column(String(6), nullable=False)
	deviceid = Column(String(6), nullable=False)
	subvendorid = Column(String(6), nullable=False)
	subdeviceid = Column(String(6), nullable=False)
	project = Column(String(255), nullable=False)
	status = Column(Enum(model.stsEnum), default=model.stsEnum.valid)

class pciresult(model.Base):
	__tablename__ = 'pciresult'
	__table_args__ = (Index('unique_constraint', "description", "vendordevice", unique=True),)
	no = Column(Integer, primary_key=True, nullable=False, unique=True)
	vendor = Column(String(45), nullable=False)
	description = Column(String(160), nullable=False)
	vendordevice = Column(String(16), nullable=False, primary_key=True)
	project = Column(String(255), nullable=False)
	exists = Column(Enum(model.estEnum), default=model.estEnum.exist)
	drivername = Column(String(160), nullable=False)
	driverversion = Column(String(60))

class logresult(model.Base):
	__tablename__ = 'logresult'
	no = Column(Integer, primary_key=True, nullable=False, unique=True)
	information = Column(BLOB, nullable=False)
	error_type = Column(Enum(model.typEnum), default=model.typEnum.error)
	source = Column(Enum(model.srcEnum), default=model.srcEnum.dmesg)
	logfile = Column(String(60), nullable=False)

class report(model.Base):
	__tablename__ = 'report'
	no = Column(Integer, primary_key=True, nullable=False, unique=True)
	#test case name
	tcname = Column(String(60), nullable=False)
	status = Column(Enum(model.rpEnum), default=model.rpEnum.Pass)
