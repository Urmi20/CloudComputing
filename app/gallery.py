from flask import render_template, session, redirect, url_for
from app.tools.dbTools import DataBaseManager
from app.tools.fileTools import FileManager
from app import userUI


@userUI.route('/gallery')
def render_gallery():
    if 'authorized' in session and session['authorized'] is True:
        dbm = DataBaseManager()
        f_mgr = FileManager()
        photos = dbm.get_user_thumbs(session['user'], f_mgr)
        img_urls = f_mgr.get_s3_url(photos)

        return render_template('gallery.html', username=session['user'], photos=img_urls)

    return redirect(url_for('index'))
