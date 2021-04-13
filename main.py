import os
from app import app
import urllib.request
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image_and_process():
	# 1.删除原来上传的文件
	for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER'], topdown=False):
		for name in files:
			os.remove(os.path.join(root, name))
		for name in dirs:
			os.rmdir(os.path.join(root, name))
	os.rmdir(app.config['UPLOAD_FOLDER'])
	os.mkdir(app.config['UPLOAD_FOLDER'])
	if 'files[]' not in request.files:
		flash('No file part')
		return redirect(request.url)
	files = request.files.getlist('files[]')
	file_names = []
	# 2.上传新文件
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_names.append(filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	# 上传保存结束，启动opensfm
	# 输出结果
	return render_template('upload.html', filenames=file_names)

@app.route('/display/<filename>')
def display_image(filename):
	print('getting',filename)
	fn = 'uploads/data_for_sfm/images/' + filename
	return redirect(url_for('static', filename=fn), code=301)

if __name__ == "__main__":
    app.run()