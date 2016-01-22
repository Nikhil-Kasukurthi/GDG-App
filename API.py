from flask import flash, redirect, url_for, session, render_template
from flask import Flask, request, redirect, url_for, jsonify
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Events, Projects
from sqlalchemy import desc
from werkzeug import secure_filename
import pyexcel.ext.xlsx



engine = create_engine('sqlite:///api.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'bitch'
app.secret_key = 'ashwiniloveskankani'
app.config['SESSION_TYPE'] = 'filesystem'


#change this for server
folder = '/home/nikhil/Desktop/GDGapp/'
ALLOWED_EXTENSIONS = set(['xlsx'])
app.config['UPLOAD_FOLDER'] = folder

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def main():
	return "Hello World"

@app.route('/events')
def events():
	items = session.query(Events).all()
	return jsonify(Events = [i.serialize for i in items])

@app.route('/events/upload',methods=['GET', 'POST'])
def upload_events():
	error = None
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			flash("Uploaded")
			session.query(Events).delete()
			flash("Deleted")
			sheet = pyexcel.get_sheet(file_name=folder+filename)
			i =1
			while (i<sheet.number_of_rows()):
				j =0
				flag = True
				while (flag!=False):
				 	Name = sheet[i,j]				 
				 	j = j+1
				 	date = sheet[i,j]
				 	j = j+1
				 	time = sheet[i,j]
				 	j= j+1
				 	venue = sheet[i,j]
				 	j = j+1
				 	speakers = sheet[i,j]
				 	j = j+1	
				 	status = sheet[i,j]
				 	j = j+1
				 	description = sheet[i,j]					 					 
				 	item = Events(name=Name,date = date, venue = venue,time = time, 
				 		speakers = speakers, status = status, description = description)
				 	session.add(item)
				 	flag = False
				i +=1
			try:
				session.commit()
				flash("Updated")
			except:
				session.rollback()
				raise				
	return render_template('upload.html',error = error)


@app.route('/projects')
def projects():
	items = session.query(Projects).all()
	return jsonify(Events = [i.serialize for i in items])

@app.route('/projects/upload',methods=['GET', 'POST'])
def upload_projects():
	error = None
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			flash("Uploaded")
			session.query(Projects).delete()
			flash("Deleted")
			sheet = pyexcel.get_sheet(file_name=folder+filename)
			i =1
			while (i<sheet.number_of_rows()):
				j =0
				flag = True
				while (flag!=False):
				 	Name = sheet[i,j]				 
				 	j = j+1
				 	lead = sheet[i,j]
				 	j = j+1
				 	members = sheet[i,j]
				 	j = j+1
				 	language = sheet[i,j]
				 	j = j+1	
				 	github = sheet[i,j]
				 	j = j+1
				 	publish_link = sheet[i,j]
				 	j = j+1
				 	description = sheet[i,j]				 					 					 
				 	item = Projects(name=Name,lead = lead,members= members, language = language, 
				 		github = github, publish_link = publish_link, description = description)
				 	session.add(item)
				 	flag = False
				i +=1
			try:
				session.commit()
				flash("Updated")
			except:
				session.rollback()
				raise				
	return render_template('upload.html',error = error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host = '0.0.0.0', port = port,debug = True)
    