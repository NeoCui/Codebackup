#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 18, 2018
toexcel.py: dump table to excel 
@author: Neo
'''
import sys
import pandas as pd
sys.path.append("/root/Project/autotest")
from sqlalchemy.inspection import inspect
from common.model import estEnum

#convert alchemy pci object to list which incluing enum type
def query_pci(rset):
	result = []
	for row in range(len(rset)):
		instance = inspect(rset[row])
		items = instance.attrs.items()
		result.append([])
		for col in range(len(items)):
			tmp = items[col][1].value
			if col == 2:
				tmp = tmp.value
			result[row].append(tmp)
	return instance.attrs.keys(), result
#convert alchemy log object to list which incluing enum type
def query_log(rset):
	result = []
	for row in range(len(rset)):
		instance = inspect(rset[row])
		items = instance.attrs.items()
		result.append([])
		for col in range(len(items)):
			tmp = items[col][1].value
			if col == 2 or col == 3:
				tmp = tmp.value
			result[row].append(tmp)
	return instance.attrs.keys(), result
#convert alchemy object to list
def query_to_list(rset):
	result = []
	for obj in rset:
		instance = inspect(obj)
		items = instance.attrs.items()
		result.append([x.value for _,x in items])
	return instance.attrs.keys(), result

#convert alchemy object to dictionary
def query_to_dict(rset):
	result = defaultdict(list)
	for obj in rset:
		instance = inspect(obj)
	for key, x in instance.attrx.items():
		result[key].append(x.value)
	return result

if __name__ == '__main__':
	print "hello"
