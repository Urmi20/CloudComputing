from flask import Flask

managerUI = Flask(__name__, template_folder='../app/templates', static_folder='../app/static')

from management import adminhome
from app import index
from app import forgotpwd
# from app import gallery
# from app import lightbox
from app import signOut
# from app import newuser
# from app import photoupload
from app.tools import dbTools
