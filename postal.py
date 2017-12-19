#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import datetime
import sys

sender = "Neo"

array1 = ((1,1234),(10,2345),(100,4312))
array2 = ((1,1234),(10,2345),(100,4312))
array3 = ((1,1234),(10,2345),(100,4312))
array4 = ((1,1234),(10,2345),(100,4312))
array5 = ((1,1234),(10,2345),(100,4312))

db = MySQLdb.connect("192.168.200.131", "game", "uu5!^%jg", "taiwan_cain_2nd")

cursor = db.cursor()

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
receiver = sys.argv[1] 
key = sys.argv[2]
choices = {'20': array1, '40': array2, '50': array3, '70': array4, '85': array5}
itemlist = choices.get(key, 'default')

for row in range(len(itemlist)):
    quantity = itemlist[row][0]
    itemid = itemlist[row][1]

    sql = "SELECT letter_id FROM postal ORDER BY id DESC limit 1"
    try:
        cursor.execute(sql)
        letterid = cursor.fetchone()
        print "Get the last letterid is '%d'" %letterid
    except:
        print "Error: unable to fetch letterid"

    letterid = letterid + 1
    sql = "INSERT INTO postal(occ_time, send_charac_name, receive_charac_no, \
	item_id, add_info, letter_id) VALUES('%s', ‘%s', '%d', '%d', '%s', '%d')" \
	(time, sender, receiver, itemid, quantity, letterid)
    try:
        cursor.execute(sql)
        db.commit()
        print "Send email succesfully"
    except:
        db.rollback()
        print "Error: Fail sending email!"

db.close()
