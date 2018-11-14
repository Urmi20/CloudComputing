from flask import g as resources
import mysql.connector
import time
from app import userUI
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from os import urandom
from base64 import b64encode

key = urandom(24)
secret_key = b64encode(key).decode('utf-8')


class DataBaseManager:
    user = "low_power"
    password = "qweQWE123!@#"
    host = "localhost"#"172.31.94.82"
    database = "InstaKilo"

    def __init__(self):
        self.db = getattr(resources, '_database', None)

        if self.db is None:
            self.db = resources._database = self._connect_to_database()

    def _connect_to_database(self):
        """This method is only supposed to be called from DataBaseManager's constructor"""
        return mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)

    def _commit(self):
        self.db.commit()

    def _run_query(self, query, parameters, auto_commit=True):
        cursor = self.db.cursor()
        rows = []
        try:
            cursor.execute(query, parameters)

            try:
                rows = cursor.fetchall()

            except mysql.connector.Error:
                # Most likely just an insert or delete query with
                # no returned results. We can ignore this error.
                pass

            if auto_commit:
                self._commit()

        except mysql.connector.Error:
            self.db.rollback()
            cursor.close()
            return False, rows

        cursor.close()
        return True, rows

    def add_user(self, username, first_name, last_name, email, password):
        query = ('insert into user (id, profile, name, first_name, last_name, email, pw_salt_hash) '
                 'values (DEFAULT, (select id from user_profile where type = "user"), %s, %s, %s, %s, %s)')
        parameters = (username, first_name, last_name, email, password)

        return self._run_query(query, parameters)[0]

    def add_photos(self, owner, title, hashtag, saved_files):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        query = ("insert into photo (id, owner, title, hashtags, date_time_added, orig_file_name, thumb_file_name) "
                 "values (DEFAULT, (select id from user where name = %s), %s, %s, %s, %s, %s)")
        parameters = (owner, title, hashtag, now, saved_files.get("original"), saved_files.get("thumbnail"))
        if not self._run_query(query, parameters, False)[0]:
            return False

        transformations = list()
        transformations.append(("warm", saved_files.get("warm")))
        transformations.append(("b&w", saved_files.get("b&w")))
        transformations.append(("high contrast", saved_files.get("high contrast")))

        for trans_type, file_name in transformations:
            query = ('insert into transformation (id, original, trans_type, file_name) '
                     'values (DEFAULT, '
                             '(select id from photo where orig_file_name = %s), '
                             '(select id from transformation_type where description = %s), '
                             '%s)')
            parameters = (saved_files.get("original"), trans_type, file_name)
            if not self._run_query(query, parameters, False)[0]:
                return False

        self._commit()

        return True

    def email_already_exists(self, email):
        query = ('select name '
                 'from user '
                 'where email = %s')
        parameters = (email,)
        return self._run_query(query, parameters)[1]

    def update_new_password(self, new_pwd, email):
        query = ('update user '
                 'set pw_salt_hash = %s '
                 'where email = %s')
        parameters = (new_pwd, email)
        print(parameters)
        return self._run_query(query, parameters)[0]

    @staticmethod
    def split_salt_hash(salt_hash):
        salt, pw_hash = salt_hash.rsplit("$", 1)
        salt = salt[1:]
        return salt, pw_hash

    def get_user_pwd_hash(self, username):
        query = ('select pw_salt_hash '
                 'from user '
                 'where name = %s')
        parameters = (username,)

        rows = self._run_query(query, parameters)[1]

        salt = pw_hash = ""

        if rows:
            salt, pw_hash = DataBaseManager.split_salt_hash(rows[0][0])

        return salt, pw_hash

    def get_user_type(self, username):
        query = ('select type from user_profile, user '
                 'where user_profile.id = user.profile and user.name = %s')
        parameters = (username,)

        rows = self._run_query(query, parameters)[1]

        return rows[0][0]

    def get_user_thumbs(self, username, f_mgr):
        query = ("select id, thumb_file_name from photo where owner = (select id from user where name = %s)"
                 "order by date_time_added desc")
        parameters = (username,)

        rows = self._run_query(query, parameters)[1]

        return rows

    def get_user_full_sizes(self, username, img_id):
        query = ("select title as transformation_type, orig_file_name "
                 "from photo where id = %s " 
                 "and owner = (select id from user where name = %s) " 
                 "UNION "
                 "select description, file_name "
                 "from transformation, photo, user, transformation_type "
                 "where original = %s and transformation.original = photo.id and " 
                 "photo.owner = (select id from user where name = %s) and " 
                 "transformation.trans_type = transformation_type.id")
        parameters = (img_id, username, img_id, username)

        rows = self._run_query(query, parameters)[1]

        return rows

    @staticmethod
    def get_token(email, expires_sec=300):
        s = Serializer(secret_key, expires_sec)
        return s.dumps({'user_id': email}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(secret_key)
        try:
            user_email = s.loads(token)['user_id']
        except:
            return None
        return user_email

    def reset_database(self):
        query = ("select title as transformation_type, orig_file_name "
                 "from photo where id = %s "
                 "and owner = (select id from user where name = %s) "
                 "UNION "
                 "select description, file_name "
                 "from transformation, photo, user, transformation_type "
                 "where original = %s and transformation.original = photo.id and "
                 "photo.owner = (select id from user where name = %s) and "
                 "transformation.trans_type = transformation_type.id")
        parameters = (img_id, username, img_id, username)

        rows = self._run_query(query, parameters)[1]

        return True


@userUI.teardown_appcontext
def teardown_db(exception):
    db = getattr(resources, "_database", None)
    if db is not None:
        db.close()
