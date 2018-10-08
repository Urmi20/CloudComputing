from flask import render_template, request, session, redirect, url_for, flash
from app.tools.pwdManager import PwdManager
from app import webapp
import os
from werkzeug.utils import secure_filename


@webapp.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    username = request.form.get('username')
    password = request.form.get('password')

    pwd_manager = PwdManager()
    if pwd_manager.check_password(username, password):
        session['user'] = username
        session['authorized'] = True
        return redirect(url_for('welcome'))

    return render_template("index.html", error=True, username=username)


@webapp.route('/welcome')
def welcome():
    if session['authorized'] is True:
        return render_template('welcome.html', username=session['user'])

    return redirect(url_for('index'))


@webapp.route('/photo_upload', methods=['POST'])
def photo_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("./app/static/UserImages", filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return redirect(request.url)


def allowed_file(filename):
    allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
