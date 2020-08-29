from datetime import datetime

import flask
from flask import render_template, flash, redirect, url_for, request
from app.forms import BeginForm, HomeForm
from werkzeug.utils import secure_filename
import os
from nlp_core.utils.general_util import draw_pie_chart_single_predict
from app import app, pc

ALLOWED_EXTENSIONS = set(['csv', 'parquet'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    last_access = datetime.utcnow()
    form = BeginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('index.html', title='Begin', form=form, last_access=last_access)


@app.route('/home', methods=['GET', 'POST'])
def home():
    form = HomeForm()
    if flask.request.method == 'POST':
        content_raw = flask.request
    result = {'category': 'Tham nhũng', 'prob': 0.96, 'content_clean': 'truong_hoc cua toi dag co nan tham_nhung'}
    content_clean = ""

    return render_template('home.html', title='Home', form=form, result=result, content_clean=content_clean)
    # return render_template()


@app.route('/home_ajax', methods=['POST'])
def home_ajax():
    data = flask.request.get_json()
    content_raw = data['content_raw']

    content_clean, result = pc.predict_single_post(content_raw)
    file_name = str(datetime.utcnow()) + '.png'
    draw_pie_chart_single_predict(result, file_name)

    # result = {'category': 'Tham nhũng', 'prob': 0.96, 'content_clean': 'truong_hoc cua toi dag co nan tham_nhung'}

    return flask.jsonify({
        'content_clean': content_clean,
        'result': result,
        'image_name': file_name
    })


@app.route('/statistic', methods=['GET', 'POST'])
def statistic():
    if request.method == "POST":
        if 'file_name' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file_load = request.files['file_name']
        if file_load.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file_load and allowed_file(file_load.filename):
            filename = secure_filename(file_load.filename)
            PATH_STORAGE_FOLDER = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_load.save(PATH_STORAGE_FOLDER)
            flash('File: ' + filename + ' successfully uploaded')
            print('File saved')
            return redirect(request.url)
        else:
            flash('File is not supported')
            return redirect(request.url)
    return render_template('statistic.html', title='Statistic')

# @app.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(secure_filename(f.filename))
#         return 'file uploaded successfully'
