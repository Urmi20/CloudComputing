from flask import session
from flask import g as user_data
from app import webapp


@webapp.before_request
def before_request():
    user_data.user = None
    user_data.authorized = None

    if 'user' in session:
        user_data.user = session['user']
    if 'authorized' in session:
        user_data.authorized = session['authorized']
