import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # BOOTSTRAP_SERVE_LOCAL = True
    KEY_TEST = 1
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/upload_file')
