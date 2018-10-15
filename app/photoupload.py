from flask import render_template, request, session, redirect, url_for
from app import webapp
from app.tools.fileTools import FileManager
from app.tools.imageTools import ImageTransform
from app.tools.dbTools import DataBaseManager
from app.tools import validate


@webapp.route('/photo_upload')
def photo_upload_landing():
    return render_template("uploadphoto.html")


@webapp.route('/photo_upload', methods=['POST'])
def photo_upload():
    if 'authorized' in session and session['authorized'] is True:
        field = validate.regex()
        owner = session["user"]
        title = field.validate(field.photo_title_pattern, request.form.get("title"))
        hashtags = field.validate(field.photo_hashtag_pattern, request.form.get("hashtags"))

        if not title:
            return render_template("gallery.html", up_error="Invalid title.", title=title, hashtags=hashtags)

        if not hashtags:
            return render_template("gallery.html", up_error="Invalid hashtags.", title=title, hashtags=hashtags)

        file_manager = FileManager()
        file = extract_photo_from_request()

        if not file or not file_manager.save_file(file):
            return render_template("gallery.html", up_error="Please select a valid file.", title=title, hashtags=hashtags)

        saved_files = ImageTransform.make_transformations(file_manager.last_saved_full_path)
        saved_files["original"] = FileManager.extract_filename(file_manager.last_saved_full_path)

        dbm = DataBaseManager()
        db_success = dbm.add_photos(owner, title, hashtags, saved_files)

        if not db_success:
            return render_template("uploadphoto.html", up_error="There was an error. Please try again.", title=title, hashtags=hashtags)

        return redirect(url_for('render_gallery'))
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
