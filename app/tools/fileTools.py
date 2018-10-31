import boto3
import botocore
import os
from app.tools.hashTools import Hash


class FileManager:
    def __init__(self):
        self.directory = "app/static/uploaded_photos/"
        self.url_for = "uploaded_photos/"
        self.allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'])
        self.last_saved_full_path = ""
        self.s3_bucket = "instakilo"

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def save_file(self, file):
        if file and self.allowed_file(file.filename):
            extension = FileManager.get_file_extension(file.filename)
            filename = FileManager.gen_unique_file_name(file.filename) + extension
            file.save(os.path.join(self.directory, filename))
            self.last_saved_full_path = os.path.join(self.directory, filename)
            return True
        return False

    def save_to_s3(self, files):
        s3 = boto3.client('s3')

        for key in files:
            filename = files[key]
            full_local_file_path = os.path.join(self.directory, filename)
            s3.upload_file(full_local_file_path, self.s3_bucket, filename)
        return True

    def download_from_s3(self, files):
        bucket = 'instakilo'  # replace with your bucket name

        s3 = boto3.resource('s3')

        for entry in files:
            file = entry[1]
            saved_file = os.path.join(self.directory, file)
            try:
                s3.Bucket(bucket).download_file(file, saved_file)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise
        return True

    def delete_file_list(self, files):
        for key in files:
            os.remove(os.path.join(self.directory, files[key]))
        return True

    @staticmethod
    def gen_unique_file_name(filename):
        salt, hashfile = Hash.get_salt_hash(filename)
        return "$" + salt + "$" + hashfile.decode("utf-8")

    @staticmethod
    def get_file_extension(filename):
        return "." + filename.split(".")[1]

    def full_path_for(self, filename):
        return self.directory+filename

    def get_url_for(self, files):
        url_for = []

        for key, file_name in files:
            url_for.append((key, os.path.join(self.url_for, file_name)))

        return url_for

    @staticmethod
    def extract_filename(full_path):
        return full_path.split("/")[-1]
