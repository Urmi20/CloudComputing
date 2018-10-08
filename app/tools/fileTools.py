import os
from werkzeug.utils import secure_filename
from app.tools.hashTools import Hash

class FileManager:
    @staticmethod
    def allowed_file(filename):
        allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])

        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def save_file(file):
        if file and FileManager.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            salt, hashfile = Hash.get_salt_hash(filename)
            filename = "$" + salt + "$" + hashfile.decode("utf-8")
            file.save(os.path.join("./app/static/UserImages", filename))
            return True
        return False
