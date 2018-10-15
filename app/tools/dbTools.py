from flask import g as resources
import mysql.connector
from app import webapp
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from os import urandom
from base64 import b64encode

key = urandom(24)
secret_key = b64encode(key).decode('utf-8')


class DataBaseManager:
    # TODO: we should not use ROOT. Create a "common" user. Can we have this data encrypted?
    user = "root"
    password = "password"
    host = "127.0.0.1"
    database = "InstaKilo"

    def __init__(self):
        self.db = getattr(resources, '_database', None)

        if self.db is None:
            self.db = resources._database = self._connect_to_database()

    def _connect_to_database(self):
        """This method is only supposed to be called from DataBaseManager's constructor"""
        return mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)

    def _run_query(self, query, parameters):
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

                self.db.commit()

        except mysql.connector.Error:
            self.db.rollback()
            cursor.close()
            return False, rows

        cursor.close()
        return True, rows

    def add_user(self, username, first_name, last_name, email, password):
        query = ('insert into users (id, profile, name, first_name, last_name, email, pw_salt_hash) '
                 'values (DEFAULT, (select id from user_profiles where type = "user"), %s, %s, %s, %s, %s)')
        parameters = (username, first_name, last_name, email, password)

        return self._run_query(query, parameters)[0]

    def email_already_exists(self, email):
        query = ('select name '
                 'from users '
                 'where email = %s')
        parameters = (email,)
        return self._run_query(query, parameters)[1]

    def update_new_password(self, new_pwd, email):
        query = ('update users '
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
                 'from users '
                 'where name = %s')
        parameters = (username,)

        rows = self._run_query(query, parameters)[1]

        salt = pw_hash = ""

        if rows:
            salt, pw_hash = DataBaseManager.split_salt_hash(rows[0][0])

        return salt, pw_hash

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


@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(resources, "_database", None)
    if db is not None:
        # TODO: Use this for debugging only. Delete this for the final release
        print("Closing DB")
        db.close()
