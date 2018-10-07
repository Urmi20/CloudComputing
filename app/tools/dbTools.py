from flask import g as resources
import mysql.connector


class DataBaseManager:

    user = "root"
    password = "password"
    host = "127.0.0.1"
    database = "InstaKilo"

    def __init__(self):
        self.db = getattr(resources, '_database', None)

        if self.db is None:
            self.db = resources._database = self.connect_to_database()

    def _connect_to_database(self):
        """This method is only supposed to be called from DataBaseManager's constructor"""
        return mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)

    @staticmethod
    def teardown_db():
        db = getattr(resources, "_database", None)

        if db is not None:
            db.close()

    def add_user(self, username, first_name, last_name, email, password):
        cursor = self.db.cursor()
        query = ('insert into users (id, profile, name, first_name, last_name, email, pw_salt_hash) '
                 'values (DEFAULT, (select id from user_profiles where type = "user"), %s, %s, %s, %s, %s)')

        cursor.execute(query, (username, first_name, last_name, email, password))

        self.db.commit()
        cursor.close()
