from cli_demo import demo
import os
from app import app
import urllib.request
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template 
from libs.config import *
from libs.pipeline import pipeline

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image_and_process():
	# 1.删除原来上传的文件
	for root, dirs, files in os.walk(data_for_sfm_dir, topdown=False):
		for name in files:
			os.remove(os.path.join(root, name))
		for name in dirs:
			os.rmdir(os.path.join(root, name))
	print('deleted')
	#os.rmdir(app.config['UPLOAD_FOLDER'])
	os.mkdir(app.config['UPLOAD_FOLDER'])
	print('mkdir')
	if 'files[]' not in request.files:
		flash('No file part')
		return redirect(request.url)
	files = request.files.getlist('files[]')
	file_names = []
	method = request.form['recon_method']
	# 2.上传新文件
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_names.append(filename)
			if method == 'fast':
				# if multi img uploaded,only save one
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'upload.jpg'))
				break
			else:
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	# main processing part
	score,percentage = pipeline(method=method,demo_show=True)
	post_method = method
	# 输出结果
	return render_template('upload.html', filenames=file_names[:1],result_score=score,result_percentage=percentage)


@app.route('/display/meshrcnn_res')
def display_meshrcnn_res():
	fn = 'uploads/data_for_sfm/images/upload.jpg'
	return redirect(url_for('static', filename=fn), code=301)

 
@app.route('/display/target')
def display_target():
	fn = 'target.jpg'
	return redirect(url_for('static', filename=fn), code=301)

@app.route('/display/help')
def display_help(): 
	fn = 'uploads/data_for_sfm/images/upload.jpg'
	return redirect(url_for('static', filename=fn), code=301)

if __name__ == "__main__":
    app.run()
