from flask import render_template, request, session, redirect, url_for
from app.tools.dbTools import DataBaseManager
from app.tools.fileTools import FileManager
from app.tools.hashTools import Hash
from app import webapp


@webapp.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    username = request.form.get('username')
    password = request.form.get('password')

    pwd_manager = Hash()
    if pwd_manager.check_password(username, password):
        session['user'] = username
        session['authorized'] = True
        return redirect(url_for('render_gallery'))

    return render_template("index.html", error=True, username=username)


@webapp.route('/gallery')
def render_gallery():
    if 'authorized' in session and session['authorized'] is True:
        dbm = DataBaseManager()
        f_mgr = FileManager()
        photos = dbm.get_user_thumbs_url(session['user'], f_mgr)

        return render_template('gallery.html', username=session['user'], photos=photos)

    return redirect(url_for('index'))
