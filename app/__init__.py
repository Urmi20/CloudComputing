from flask import Flask

webapp = Flask(__name__)

from app import index
from app import forgotpwd


