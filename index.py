import os
from json import dumps
from flask import Flask, flash, request
from flask import redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from src import api

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def _index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        match_finder = api.MatchFinder()
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
            file_path = os.path.join('imgs', filename)
            file_.save(file_path)
            name, image_path = match_finder.find(file_path)
            print name, image_path
            return dumps({'result': 'OK', 'url': image_path, 'name': name})

        return render_template('index.html')

@app.route('/images/<path:filename>')
def download_file(filename):
    return send_file('./images/' + filename)
app.run(port=5000, debug=True)
