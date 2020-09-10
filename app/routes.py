from datetime import datetime

import time
import flask
from flask import render_template, flash, redirect, url_for, request, session, send_file
from app.forms import BeginForm, HomeForm
from werkzeug.utils import secure_filename
from nlp_core.config.conf_params import get_path_saved_result_file, get_label_by_IID, get_path_result_from_filename
from nlp_core.utils.general_normalize import _clean_text
from nlp_core.utils.general_util import _load_model, _load_vectorizer, _convert_ndarray_data, draw_prob_number_posts, \
    draw_prob_number_users, draw_prob_number_access, draw_prob_each_user, remove_all_files_folder
import os
import pandas as pd
import csv
from nlp_core.utils.general_util import draw_pie_chart_single_predict
from app import app, pc

ALLOWED_EXTENSIONS = set(['csv'])


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
    # get from ajax process 'statistic.js'
    content_raw = data['content_raw']

    import time
    time_start = time.time()
    content_clean, result = pc.predict_single_post(content_raw)
    print('time to process: {}'.format(time.time() - time_start))
    file_name = 'image_single_predict_' + str(time.time()) + '.png'
    draw_pie_chart_single_predict(result, file_name)

    # result = {'category': 'Tham nhũng', 'prob': 0.96, 'content_clean': 'truong_hoc cua toi dag co nan tham_nhung'}

    return flask.jsonify({
        'content_clean': content_clean,
        'result': result,
        'image_name': file_name
    })


@app.route('/statistic', methods=['GET', 'POST'])
def statistic():
    PATH_STORAGE_FOLDER = None
    PATH_DOWNLOADED = None
    FILE_DOWNLOADED_NAME = None
    path_file_name_display_number_posts = None
    path_file_name_display_number_users = None
    path_file_name_display_number_access = None
    if request.method == "POST":
        if request.form['btn'] == 'btn-upload-file':
            if 'file_name' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file_load = request.files['file_name']
            if file_load.filename == '':
                flash('No file selected for uploading')
                return redirect(request.url)
            if file_load and allowed_file(file_load.filename):
                filename = secure_filename(file_load.filename)
                base_filename = filename.split(".")[0]
                filename = f"{base_filename}_{int(time.time())}.csv"
                PATH_STORAGE_FOLDER = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_load.save(PATH_STORAGE_FOLDER)
                flash('File: ' + filename + ' successfully uploaded')
                print('File saved: ' + PATH_STORAGE_FOLDER)
                # return 1
                # return redirect(request.url)
                # return redirect(url_for('process_file', filepath=PATH_STORAGE_FOLDER))
            else:
                flash('File is not supported')
                return redirect(request.url)
        elif request.form['btn'] == 'btn-process-file':
            print(request.args)

            # READ FILE CSV
            filepath = request.args.get('path_main', 'undef')
            print(filepath)
            # filepath = '/home/trunganh/TrungAnh/CyberspaceCombat/CyberspaceCombat/app/static/upload_file/test_data.csv'
            if filepath != 'undef':
                df_raw = pd.read_csv(filepath, delimiter='|')
                print(df_raw.head(2))

                print('Processing...')
                index_ = 0
                total_row = len(df_raw)
                iter_ = total_row / 10000
                if iter_ < 5:
                    iter_ = 5
                # test
                iter_ = 1
                PATH_DOWNLOADED = get_path_saved_result_file(filepath)
                FILE_DOWNLOADED_NAME = os.path.basename(PATH_DOWNLOADED)
                with open(PATH_DOWNLOADED, 'w', encoding='utf-8') as f:
                    f_writer = csv.writer(f, delimiter='|')
                    f_writer.writerow(
                        ['author_id', 'post_id', 'content_clean', 'category', 'prob'])
                    for row in df_raw.itertuples():
                        index_ += 1
                        if index_ % iter_ == 0:
                            session.pop('_flashes', None)
                            flash('Processing... {}%'.format(index_ / total_row))
                        x_clean = _clean_text(row.content_raw)
                        x_np = _convert_ndarray_data(pc.vectorizer, x_clean)
                        x_predict = pc.model.predict(x_np).squeeze().tolist()
                        prob = pc.model.predict_proba(x_np)[0].tolist()
                        result = {get_label_by_IID(str(index)): prob[index] for index in range(0, len(x_predict)) if
                                  x_predict[index] == 1}
                        for k, v in result.items():
                            f_writer.writerow([row.author_id, row.post_id, x_clean, k, v])
                    session.pop('_flashes', None)
                    flash('Finish processing')

                # Statistic
                df_result = pd.read_csv(PATH_DOWNLOADED, delimiter='|')
                file_name_number_posts = 'output_prob_post_' + os.path.basename(filepath) + '.png'
                file_name_number_users = 'output_prob_user_' + os.path.basename(filepath) + '.png'
                file_name_number_access = 'output_prob_access_' + os.path.basename(filepath) + '.png'

                draw_prob_number_posts(df_result, file_name_number_posts)
                draw_prob_number_users(df_result, file_name_number_users)
                draw_prob_number_access(df_result, file_name_number_access)
                # ======
                path_file_name_display_number_posts = '/static/output_chart/output_prob_post/' + file_name_number_posts
                path_file_name_display_number_users = '/static/output_chart/output_prob_user/' + file_name_number_users
                path_file_name_display_number_access = '/static/output_chart/output_prob_access/' + file_name_number_access

            else:
                flash('file is not uploaded')
            # print('process_fileeeeee: ' + filepath)
    return render_template('statistic.html', title='Statistic',
                           path_file=PATH_STORAGE_FOLDER,
                           path_download=PATH_DOWNLOADED,
                           file_name_number_posts=path_file_name_display_number_posts,
                           file_name_number_users=path_file_name_display_number_users,
                           file_name_number_access=path_file_name_display_number_access,
                           file_downloaded_name=FILE_DOWNLOADED_NAME)


# @app.route('/statistic/<filepath>', methods=['GET'])
# def process_file(filepath):
#     print('path_filesss: ' + filepath)
#     return redirect(url_for('statistic'))

# @app.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(secure_filename(f.filename))
#         return 'file uploaded successfully'

@app.route('/download_file', methods=['GET'])
def download_file():
    path = request.args.get('path', None)
    if path is None:
        flash('path is None')
        redirect(url_for('statistic'))
    else:
        try:
            print('test:---' + path)
            return send_file(path, as_attachment=True)
        except Exception as e:
            print(e)
            flash('error 404')
            print('test error:---' + path)
            redirect(url_for(statistic))
            raise e


@app.route('/statistic_ajax', methods=['POST'])
def statistic_ajax():
    data = flask.request.get_json()
    hidden_file_name_output = data['hidden_file_name_output']
    id_user = data['id_user']

    file_path_result_csv = get_path_result_from_filename(hidden_file_name_output)
    print('output_hidden = {}'.format(file_path_result_csv))
    file_name_statistic_user = 'output_prob_each_user_' + os.path.basename(file_path_result_csv) + '.png'

    df_result = pd.read_csv(file_path_result_csv, delimiter='|')
    df_final = df_result[df_result['author_id'].astype(str).str.match(id_user)]
    print('id ======')
    print(id_user)
    print(df_final.info())
    print(type(id_user))
    if len(df_final) > 0:
        status = 'success'
        # draw
        print('len > 0')
        draw_prob_each_user(df_final, file_name_statistic_user)
    else:
        print('len < 0')
        status = 'id not found'

    return flask.jsonify({
        'status': status,
        'image_name': file_name_statistic_user
    })
