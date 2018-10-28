from flask import render_template, session, redirect, url_for
from app.tools.dbTools import DataBaseManager
from app.tools.fileTools import FileManager
from app import userUI


@userUI.route('/gallery')
def render_gallery():
    if 'authorized' in session and session['authorized'] is True:
        dbm = DataBaseManager()
        f_mgr = FileManager()
        photos = dbm.get_user_thumbs_url(session['user'], f_mgr)

        return render_template('gallery.html', username=session['user'], photos=photos)

    return redirect(url_for('index'))
