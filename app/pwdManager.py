from hashlib import pbkdf2_hmac
from os import urandom
from binascii import hexlify


# TODO: define a __str__ method, a __repr__ method and a __init__ if needed
class PwdObfuscation:
    def getsaltedhash(self, password):

        # TODO: define constants
        salt = urandom(16)
        dk = pbkdf2_hmac("sha512", password.encode(), salt, 100000)
        return hexlify(dk), salt
