from flask import render_template, session, url_for, redirect
from app.tools.dbTools import DataBaseManager
from app.tools.fileTools import FileManager
from app import userUI


@userUI.route('/light_box/<id>', methods=['GET'])
def render_light_box(id):
    if 'authorized' in session and session['authorized'] is True:
        dbm = DataBaseManager()
        f_mgr = FileManager()
        photos = dbm.get_user_full_sizes(session['user'], id)
        img_urls = f_mgr.get_s3_url(photos)

        if photos:
            return render_template('lightbox.html', username=session['user'], photos=img_urls)

    return redirect(url_for('index'))