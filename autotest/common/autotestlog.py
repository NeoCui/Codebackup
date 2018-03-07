#!/usr/bin/python
# -*- encoding: utf-8 -*-
#logging.py: logging initialization file
#created on Jan 17, 2018
#author: Neo
import logging, os
import logging.handlers

# create logger
logger_name = "autotest"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

# create file handler
log_path = "/var/log/autotest"
isExists = os.path.exists(log_path)
if not isExists:
	os.makedirs(log_path)
else:
	pass
log_file = log_path+"/autotest.log"
fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=40)

# create formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

# add handler and formatter to logger
fh.setFormatter(formatter)
logger.addHandler(fh)

