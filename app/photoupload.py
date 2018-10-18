from flask import render_template, request, session, redirect, url_for, Response
from app import webapp
from app.tools.fileTools import FileManager
from app.tools.imageTools import ImageTransform
from app.tools.hashTools import Hash
from app.tools.dbTools import DataBaseManager
from app.tools import validate


@webapp.route('/photo_upload')
def photo_upload_landing():
    if 'authorized' in session and session['authorized'] is True:
        return render_template("uploadphoto.html")
    else:
        return redirect(url_for('index'))


@webapp.route('/photo_upload', methods=['POST'])
def photo_upload():
    if 'authorized' in session and session['authorized'] is True:
        input_title = request.form.get("title")
        input_hashtags = request.form.get("hashtags")

        field = validate.regex()
        owner = session["user"]
        title = field.validate(field.photo_title_pattern, input_title)
        hashtags = field.validate(field.photo_hashtag_pattern, input_hashtags)

        if not title:
            return render_template("uploadphoto.html",
                                   up_error="Invalid title. Hover cursor over field for requirements.",
                                   title=input_title, hashtags=input_hashtags)

        if not hashtags:
            return render_template("uploadphoto.html",
                                   up_error="Invalid hashtags. Hover cursor over fields for requirements.",
                                   title=input_title, hashtags=input_hashtags)

        file_manager = FileManager()
        file = extract_photo_from_request()

        if not file or not file_manager.save_file(file):
            return render_template("uploadphoto.html",
                                   up_error="Please select a valid file.", title=title, hashtags=hashtags)

        saved_files = ImageTransform.make_transformations(file_manager.last_saved_full_path)
        saved_files["original"] = FileManager.extract_filename(file_manager.last_saved_full_path)

        dbm = DataBaseManager()
        db_success = dbm.add_photos(owner, title, hashtags, saved_files)

        if not db_success:
            return render_template("uploadphoto.html",
                                   up_error="There was an error. Please try again.", title=title, hashtags=hashtags)

        return redirect(url_for('render_gallery'))
    return redirect(url_for('index'))


def extract_photo_from_request():
    if request.method != 'POST':
        return None

    # Checking for file contents
    if 'uploadedfile' not in request.files:
        return None
    file = request.files['uploadedfile']
    # Checking for "no selection"
    if file.filename == '':
        return None

    return file


@webapp.route('/test/FileUpload', methods=['POST'])
def test_upload():
    userID = request.form.get("userID")
    password = request.form.get("password")
    file = extract_photo_from_request()

    pwd_manager = Hash()
    if not pwd_manager.check_password(userID, password):
        return Response(status=401)

    file_manager = FileManager()
    if not file or not file_manager.save_file(file):
        return Response(status=400)

    saved_files = ImageTransform.make_transformations(file_manager.last_saved_full_path)
    saved_files["original"] = FileManager.extract_filename(file_manager.last_saved_full_path)

    dbm = DataBaseManager()
    db_success = dbm.add_photos(userID, "Auto Uploaded", "#test_image", saved_files)

    if db_success:
        return Response(status=200)
    else:
        return Response(status=500)
