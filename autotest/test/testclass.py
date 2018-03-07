#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 09, 2018
testclass.py: sqlalchemy testing class
@author: Neo
'''
import sys
sys.path.append("/root/Project/autotest")
from sqlalchemy import * 
from common import model

from datetime import datetime

class Test(model.Base):
	__tablename__ = 'test_table'
	__table_args__ = (Index('unique_key_val', "key", "val", unique=True),)
	id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
	key = Column(String(30), nullable=False)
	val = Column(String(60))
	information = Column(Text, nullable=False)
	date = Column(DateTime, default=datetime.utcnow)

