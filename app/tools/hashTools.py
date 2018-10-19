from hashlib import pbkdf2_hmac
from binascii import hexlify
import uuid
from app.tools.dbTools import DataBaseManager


class Hash:
    @staticmethod
    def get_salt_hash(string, salt=None):

        if salt is None:
            salt = uuid.uuid4().hex

        dk = pbkdf2_hmac("sha512", string.encode(), salt.encode(), 100000)
        return salt, hexlify(dk)

    @staticmethod
    def check_password(username, password):
        dbm = DataBaseManager()
        db_salt, db_pw_hash = dbm.get_user_pwd_hash(username)

        pw_hash = Hash.get_salt_hash(password, db_salt)[1]

        if db_pw_hash == pw_hash.decode("utf-8"):
            return True

        return False
