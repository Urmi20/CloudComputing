from flask import Flask

webapp = Flask(__name__)

from app import index
from app import forgotpwd
from app import welcome
from app import requestCommon
from app import signOut