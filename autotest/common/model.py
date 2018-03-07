#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 09, 2018
model.py: sqlalchemy model file 
@author: Neo
'''
import enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

#platform enum:
class plmEnum(enum.Enum):
	x86_64	= 'x86_64'
	i386	= 'i386'
	i686	= 'i686'

#series enum:
class srsEnum(enum.Enum):
	thinkserver	= 'thinkserver'
	systemx		= 'systemx'
	thinksystem	= 'thinksystem'

#type enum:
class typEnum(enum.Enum):
	error	= 'error'
	warning	= 'warning'
	fail	= 'fail'

#source enum:
class srcEnum(enum.Enum):
	dmesg		= 'dmesg'
	messages	= 'messages'
	mcelog		= 'mcelog'
	x11			= 'x11'
	anaconda	= 'anaconda'
	yast		= 'yast'

#status enum:
class stsEnum(enum.Enum):
	valid	= 'valid'
	invalid	= 'invalid'

#isexist enum:
class estEnum(enum.Enum):
	exist	= 'exist'
	NA		= 'NA'

#bios mode enum:
class modEnum(enum.Enum):
	UEFI	= 'UEFI'
	Legacy	= 'Legacy'

#testcase status
class rpEnum(enum.Enum):
	Pass = 'Pass'
	Fail = 'Fail'

#find the Nth occurred substring position in the string
def findSubstring(string, substring, times):
	current = 0
	for i in range(1, times+1):
		current = string.find(substring, current)+1
		if current == 0:
			return -1
	return current-1

#base class for creating class
Base = declarative_base()
#connect to the database
def connectDB():
	print "Create database engine..."
	engine = create_engine('mysql+mysqlconnector://root:111111@10.245.39.75:3306/test', echo=True)
	print "Done."
	return engine
