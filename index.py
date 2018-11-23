from json import dumps
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def _index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print request.files
        # check if the post request has the file part
        if 'fileToUpload' not in request.files:
            print 'No file part'
            return redirect(request.url)
        file_ = request.files['fileToUpload']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file_.filename == '':
            print 'No selected file'
            return redirect(request.url)
        if file_:
            filename = secure_filename(file_.filename)
            file_.save(os.path.join('imgs', filename))
            return dumps({'result': 'OK', 'url': '/images/default.jpg'})
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

app.run(port=5000, debug=True)
