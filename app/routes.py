from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from app.forms import HomeForm
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    last_access = datetime.utcnow()
    form = HomeForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('index.html', title='Begin', form=form, last_access=last_access)


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')
    # return render_template()
