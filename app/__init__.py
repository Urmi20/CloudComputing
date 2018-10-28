from flask import Flask

userUI = Flask(__name__)

from app import index
from app import forgotpwd
from app import gallery
from app import lightbox
from app import signOut
from app import newuser
from app import photoupload
from app.tools import dbTools
