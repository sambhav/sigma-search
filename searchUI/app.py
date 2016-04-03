import os
from flask import Flask, render_template, request, json,redirect, url_for, send_from_directory
from werkzeug import secure_filename
from searchMethods import *


app = Flask(__name__)

#Upload Folder
app.config['UPLOAD_FOLDER'] = 'uploads/'
#To allow only Image Uploads
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#Function to find the extension of an uploaded file
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
#Main Page
@app.route('/')
def searchpage():
	return render_template('Search.html')

#Handling Search Queries
@app.route('/search', methods=['POST'])
def searchresults():
	searchQ =  request.form['searchq']
	searchType=request.form['activeTab']
	result=[]    
	if searchType=="Search":
		result=pagesearch(searchQ)
	elif searchType=="Document":
		result=docsearch(searchQ)     
	elif searchType=="Image":
		result=imgsearch(searchQ)  
	return json.dumps({'status':'OK','search':result})


#Reverse Search Page
@app.route('/Reverse')
def index():
	return render_template('Revimg.html')

#Handling Image Uploads
@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		result=revimg(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return json.dumps({'status':'OK','search':result})

if __name__=="__main__":
	app.run(host='0.0.0.0')
