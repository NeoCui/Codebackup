#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Mar 5, 2018
webapp.py: website provider
@author: Neo
'''
import sys, os, md5
sys.path.append("/root/Project/autotest")
from flask import Flask, redirect, render_template, request, session, json
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlserver import SQLClass
from common import model

#database connection
engine = model.connectDB()
print "Create database session..."
Session = sessionmaker(bind=engine)
db_session = Session()
print "Done."
print "Create metadata object..."
meta = MetaData(bind=engine)
meta.reflect(bind=engine)
model.Base.metadata.create_all(engine, checkfirst=True)
print "Done."

#app initialization
app = Flask(__name__)

#webpage initialization
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
	if session.get('logged_in'):
		return render_template('home.html')
	else:
		return error('Unauthorized access')

@app.route('/log')
def log():
	if session.get('logged_in'):
		return render_template('log.html', username=session.get('logged_in'))
	else:
		return error('Unauthorized access')

@app.route('/device')
def device():
	if session.get('logged_in'):
		return render_template('device.html', username=session.get('logged_in'))
	else:
		return error('Unauthorized access')

@app.route('/error')
def error(info):
    return render_template('error.html', error=info)

@app.route("/logout")
def logout():
    db_session.close()
    session.pop('logged_in', None)
    return login()
#end webpage initialization


#user sign in interface
#function: do_admin_login
@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    mdobj = md5.new()
    mdobj.update(POST_PASSWORD)
    mdobj = mdobj.hexdigest()

    query = db_session.query(SQLClass.user).filter(SQLClass.user.username.in_([POST_USERNAME]))
    result = query.first()
    if result:
		if mdobj!=result.password or request.form['username']!=result.username:
			return error('Wrong Credentials!')
		else:
			session['logged_in'] = result.firstname + result.lastname 
			return home()
    else:
		return error("user doesn't exist!")
#end do_admin_login()

#user sign up interface
#function: register
@app.route('/register', methods=['POST'])
def register():
    POST_FNAME = str(request.form['fname'])
    POST_LNAME = str(request.form['lname'])
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    mdobj = md5.new()
    mdobj.update(POST_PASSWORD)
    mdobj = mdobj.hexdigest()
    new_user = SQLClass.user(firstname=POST_FNAME, lastname=POST_LNAME, username=POST_USERNAME, password=mdobj)
    try:
		db_session.add(new_user)
		db_session.commit()
		return error('Register Succeed!')
    except Exception as e:
		db_session.rollback()
		if e.message.find("Duplicate entry") > 0:
			return error("Already existed account!")
    return error("Register Failed!")
#end register

#Start log information handle section
#show new html page (addlog.html) bind with  add log interface
#function: showAddLog
@app.route('/showAddLog')
def showAddLog():
	if session.get('logged_in'):
		return render_template('addlog.html')
	else:
		return error('Unauthorized Access')
#end showAddLog

#get log information by logid called by log.html operation - edit log
#function: getLogById
@app.route('/getLogById',methods=['POST'])
def getLogById():
    try:
        if session.get('logged_in'):
			POST_ID = request.form['logid'] 
			query = db_session.query(SQLClass.log).filter(SQLClass.log.logid==POST_ID).first()
			if query:
				record = []
				record.append({'Id':query.logid,'Information':query.information,'Comment':query.comment,'Status':query.status.value})
				return json.dumps(record)
			else:
				return error('Record not found.')
        else:
            return error('Unauthorized Access')
    except Exception as e:
        return error(str(e))
#end getLogById

#log.html operation - update log
#function: updateLog
@app.route('/updateLog', methods=['POST'])
def updateLog():
    try:
        if session.get('logged_in'):
			_comment = request.form['comment']
			_status = request.form['stat']
			_log_id = request.form['logid']
			query = db_session.query(SQLClass.log).filter(SQLClass.log.logid==_log_id).first()
			query.comment = _comment
			query.status = _status 
			try:
				db_session.commit()
				return json.dumps({'status':'OK'})
			except Exception as e:
				db_session.rollback()
				return json.dumps({'status':'ERROR'})
        else:
            return error('Unauthorized Access')
    except Exception as e:
        return json.dumps({'status': str(e)})
#end updateLog

#log.html operation - delete log
#function: deleteLog
@app.route('/deleteLog',methods=['POST'])
def deleteLog():
    try:
		if session.get('logged_in'):
			POST_ID = request.form['logid']
			query = db_session.query(SQLClass.log).filter(SQLClass.log.logid==POST_ID).first()
			try:
				db_session.delete(query)
				db_session.commit()
				return json.dumps({'status':'OK','Id': POST_ID})
			except Exception as e:
				db_session.rollback()
				return json.dumps({'status':'An Error occured'})
		else:
			return error('Unauthorized Access')
    except Exception as e:
		return json.dumps({'status':str(e)})
#end deleteLog

#get all the log information from database
#and show them on the html table
#function: getLog
@app.route('/getLog', methods=['GET'])
def getLog():
    try:
		if session.get('logged_in'):
			query = db_session.query(SQLClass.log).order_by(SQLClass.log.logid)
			records_dict = []
			for item in query.all():
				record_dict = {
                        'Id': item.logid,
                        'Comment': item.comment,
                        'Information': item.information,
                        'Error_Type': item.error_type.value,
						'Status': item.status.value}
				records_dict.append(record_dict)

			return json.dumps(records_dict)
		else:
			return error('Unauthorized Access')
    except Exception as e:
        return error(str(e))
#end getLog

#add new log interface on addlog.html
#function: addLog
@app.route('/addLog',methods=['POST'])
def addLog():
    try:
        if session.get('logged_in'):
			_information = request.form['inputInfo']
			_error_type = request.form['inputError_Type']
			_source = request.form['inputSrc']
			_status = request.form['inputStat']
			_comment = request.form['inputComment']
			mdobj = md5.new()
			mdobj.update(_information)
			mdobj = mdobj.hexdigest()
			new_record = SQLClass.log(information=_information, error_type=_error_type, source=_source, comment=_comment, \
					status=_status, md5=mdobj)
			try:
				db_session.add(new_record)
				db_session.commit()
				return log() 
			except Exception as e:
				db_session.rollback()
				if e.message.find("Duplicate entry") < 0:
					return error(str(e))
        else:
            return error('Unauthorized Access')
    except Exception as e:
        return error(str(e))
#end addLog
#end log information handle section

#Start device (pciid) information handle section
#show new html page (device.html) to add new device pciid information
#function: showAddDevice
@app.route('/showAddDevice')
def showAddDevice():
	if session.get('logged_in'):
		return render_template('adddevice.html')
	else:
		return error('Unauthorized Access')
#end showAddDevice

#get device information by deviceid (pciidid) called by device operation - 
#edit and delete
#function: getDeviceById
@app.route('/getDeviceById',methods=['POST'])
def getDeviceById():
    try:
        if session.get('logged_in'):
			POST_ID = request.form['pciidid'] 
			query = db_session.query(SQLClass.pciid).filter(SQLClass.pciid.pciidid==POST_ID).first()
			if query:
				record = []
				record.append({'Id':query.pciidid,'Vendor':query.vendor,'Description':query.description,'Vendorid':query.vendorid,'Deviceid':query.deviceid,'Subvendorid':query.subvendorid,'Subdeviceid':query.subdeviceid,'Project':query.project,'Status':query.status.value})
				return json.dumps(record)
			else:
				return error('Record not found.')
        else:
            return error('Unauthorized Access')
    except Exception as e:
        return error(str(e))
#end getDeviceById

#device.html operation - edit one device information
#function: updateDevice
@app.route('/updateDevice', methods=['POST'])
def updateDevice():
    try:
        if session.get('logged_in'):
			_project = request.form['inputPro']
			_vid = request.form['vendorid']
			_did = request.form['deviceid']
			_svid = request.form['subvendorid']
			_sdid = request.form['subdeviceid']
			_status = request.form['inputStat']
			_pci_id = request.form['pciidid']
			query = db_session.query(SQLClass.pciid).filter(SQLClass.pciid.pciidid==_pci_id).first()
			query.project = _project
			query.vendorid = _vid
			query.deviceid = _did
			query.subvendorid = _svid
			query.subdeviceid = _sdid
			query.status = _status
			try:
				db_session.commit()
				return json.dumps({'status':'OK'})
			except Exception as e:
				db_session.rollback()
				return json.dumps({'status':'ERROR'})
        else:
            return error('Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
#end updateDevice

#device.html oeration - delete one device information
#function: deleteDevice
@app.route('/deleteDevice',methods=['POST'])
def deleteDevice():
    try:
		if session.get('logged_in'):
			POST_ID = request.form['pciidid']
			query = db_session.query(SQLClass.pciid).filter(SQLClass.pciid.pciidid==POST_ID).first()
			try:
				db_session.delete(query)
				db_session.commit()
				return json.dumps({'status':'OK','Id': POST_ID})
			except Exception as e:
				db_session.rollback()
				return json.dumps({'status':'An Error occured'})
		else:
			return error('Unauthorized Access')
    except Exception as e:
		return json.dumps({'status':str(e)})
#end deleteDevice

#get all the device information from database
#and show them on the html table
#fucntion: getDevice
@app.route('/getDevice', methods=['GET'])
def getDevice():
    try:
		if session.get('logged_in'):
			query = db_session.query(SQLClass.pciid).order_by(SQLClass.pciid.pciidid)
			records_dict = []
			for item in query.all():
				record_dict = {
                        'Id': item.pciidid,
                        'Vendor': item.vendor,
                        'Description': item.description,
                        'Vendorid': item.vendorid,
                        'Deviceid': item.deviceid,
                        'Subvendorid': item.subvendorid,
                        'Subdeviceid': item.subdeviceid,
						'Project': item.project,
						'Status': item.status.value}
				records_dict.append(record_dict)

			return json.dumps(records_dict)
		else:
			return error('Unauthorized Access')
    except Exception as e:
        return error(str(e))
#end getDevice

#add new device information on adddevice.html
#function: addDevice
@app.route('/addDevice',methods=['POST'])
def addDevice():
    try:
        if session.get('logged_in'):
			_vendor = request.form['inputVendor']
			_project = request.form['inputPro']
			_description = request.form['inputDes']
			_vid = request.form['vendorid']
			_did = request.form['deviceid']
			_svid = request.form['subvendorid']
			_sdid = request.form['subdeviceid']
			_status = request.form['inputStat']
			new_record = SQLClass.pciid(vendor=_vendor, description=_description, vendorid=_vid, deviceid=_did, \
					subvendorid=_svid, subdeviceid=_sdid, project=_project, status=_status)
			try:
				db_session.add(new_record)
				db_session.commit()
				return device() 
			except Exception as e:
				db_session.rollback()
				if e.message.find("Duplicate entry") < 0:
					return error(str(e))
        else:
            return error('Unauthorized Access')
    except Exception as e:
        return error(str(e))
#end addDevice
#end device information handle section

#main fucntion
if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	host_ip = '10.245.39.75' 
	host_port = 8000
	app.run(debug=True, host=host_ip, port=host_port)
