from flask import g as resources
import mysql.connector
from app import webapp


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

    @staticmethod
    def teardown_db():
        db = getattr(resources, "_database", None)

        if db is not None:
            db.close()

    # TODO: Try using a variadic function to have all the "run queries" in common code
    def add_user(self, username, first_name, last_name, email, password):
        cursor = self.db.cursor()
        query = ('insert into users (id, profile, name, first_name, last_name, email, pw_salt_hash) '
                 'values (DEFAULT, (select id from user_profiles where type = "user"), %s, %s, %s, %s, %s)')

        try:
            cursor.execute(query, (username, first_name, last_name, email, password))
            self.db.commit()
        except mysql.connector.Error as err:
            # TODO: Can we be more restrictive with this except? Currently it is too broad.
            self.db.rollback()
            cursor.close()
            print(err)
            return False

        cursor.close()
        return True

    def get_user_pwd_hash(self, username):
        cursor = self.db.cursor()
        query = ('select pw_salt_hash '
                 'from users '
                 'where name = %s')

        try:
            cursor.execute(query, (username,))
        except mysql.connector.Error as err:
            print(err)
            cursor.close()
            return "", ""

        row = cursor.fetchone()

        salt = pw_hash = ""

        if row is not None:
            salt_hash = row[0]

            salt, pw_hash = salt_hash.rsplit("$", 1)
            salt = salt[1:]
            cursor.close()

        return salt, pw_hash


@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(resources, "_database", None)
    if db is not None:
        # TODO: Use this for debugging only. Delete this for the final release
        print("Closing DB")
        db.close()
