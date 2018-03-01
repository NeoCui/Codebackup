from flask import Flask, flash, redirect, render_template, request, session, url_for
import os, md5
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysqlconnector://root:111111@10.245.39.75:3306/test', echo=True)
Base = declarative_base()

class User(Base):
	__tablename__ = 'User'
	__table_args__ = (Index('unique_constratint', "username", unique=True),)
	userid = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
	firstname = Column(String(32), nullable=False)
	lastname = Column(String(32), nullable=False)
	username = Column(String(64), nullable=False)
	password = Column(String(64), nullable=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
db_session = Session()

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    mdobj = md5.new()
    mdobj.update(POST_PASSWORD)
    mdobj = mdobj.hexdigest()

    query = db_session.query(User).filter(User.username.in_([POST_USERNAME]))
    result = query.first()
    print mdobj
    print result.password
    if mdobj!=result.password or request.form['username']!=result.username:
		session['logged_in'] = False
    else:
        session['logged_in'] = True
        return redirect(url_for('index'))
    return "Wrong credentials! Please retry it again! <a href='/logout'>Back</a>"

@app.route('/register', methods=['POST'])
def register():
    POST_FNAME = str(request.form['fname'])
    POST_LNAME = str(request.form['lname'])
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    mdobj = md5.new()
    mdobj.update(POST_PASSWORD)
    mdobj = mdobj.hexdigest()
    new_user = User(firstname=POST_FNAME, lastname=POST_LNAME, username=POST_USERNAME, password=mdobj)
    try:
		db_session.add(new_user)
		db_session.commit()
		return "Congratulations! You now can sign in with your registered information.<br> <a href='/logout'>Back</a>"
    except Exception as e:
		db_session.rollback()
		if e.message.find("Duplicate entry") < 0:
			flash('Duplicated username!')
    return "Register failed! Please retry it again! <a href='/logout'>Back</a>"

@app.route("/logout")
def logout():
    db_session.close()
    session['logged_in'] = False
    return login()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='10.245.39.75', port=8000)
