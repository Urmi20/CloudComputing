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
        f_mgr.download_from_s3(photos)
        img_urls = f_mgr.get_url_for(photos)

        return render_template('gallery.html', username=session['user'], photos=img_urls)

    return redirect(url_for('index'))
