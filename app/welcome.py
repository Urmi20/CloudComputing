from flask import render_template, request, session, redirect, url_for
from app.tools.hashTools import Hash
from app import webapp
from app.tools.fileTools import FileManager


@webapp.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    username = request.form.get('username')
    password = request.form.get('password')

    pwd_manager = Hash()
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


def extract_photo_from_request():
    if request.method != 'POST':
        return None

    # Checking for file contents
    if 'file' not in request.files:
        return None
    file = request.files['file']
    # Checking for "no selection"
    if file.filename == '':
        return None

    return file


@webapp.route('/photo_upload', methods=['POST'])
def photo_upload():
    file = extract_photo_from_request()

    if not file or not FileManager.save_file(file):
        return render_template("welcome.html", up_error="Please select a valid file.")

    return redirect(url_for('uploaded_file', filename=file.filename))
