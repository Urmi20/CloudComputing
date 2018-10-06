from app import webapp
from flask import render_template


@webapp.route('/newuser')
def create_user_landing():
    return render_template("newuser.html", username=None,  first_name=None, last_name=None,
                           email=None, password=None, password_conf=None)


@webapp.route('/newuser/create', methods=['POST'])
def create_user():
    return None