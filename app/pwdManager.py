from hashlib import pbkdf2_hmac
from os import urandom
from binascii import hexlify


# TODO: define a __str__ method, a __repr__ method and a __init__ if needed
class PwdManager:
    def get_salt_hash(self, password, salt=None):

        # TODO: define constants
        if salt is None:
            salt = urandom(16)

        dk = pbkdf2_hmac("sha512", password.encode(), salt, 100000)
        return salt, hexlify(dk)

    # TODO: Actually get the salt and the coded password from the database
    # TODO: Hash the password (arg) using the DB salt (call get_salt_hash())
    def check_password(self, username, password):
        if password == 'password':
            return True

        return False
