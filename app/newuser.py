from flask import render_template, request, redirect, url_for, session
from app import webapp
from app.tools import validate
from app.tools.dbTools import DataBaseManager
from app.tools.hashTools import Hash


@webapp.route('/newuser')
def create_user_landing():
    return render_template("newuser.html", username=None,  first_name=None, last_name=None,
                           email=None, password=None, password_conf=None)


@webapp.route('/newuser/create', methods=['POST'])
def create_user():
    field = validate.regex()
    username = field.validate(field.user_name_pattern, request.form.get("username"))
    first_name = field.validate(field.first_name_pattern, request.form.get("first_name"))
    last_name = field.validate(field.last_name_pattern, request.form.get("last_name"))
    email = field.validate(field.email_pattern, request.form.get("email"))
    password = field.validate(field.password_pattern, request.form.get("password"))
    password_conf = password == request.form.get("password_conf")

    err_msg = compose_error_message(username, first_name, last_name, email, password, password_conf)

    if err_msg is not None:
        return render_template("newuser.html", error=err_msg, username=username, first_name=first_name,
                               last_name=last_name, email=email, password=password, password_conf=password_conf)

    pwd_manager = Hash()
    salt, hashpwd = pwd_manager.get_salt_hash(password)
    stored_pwd = "$" + salt + "$" + hashpwd.decode("utf-8")

    dbm = DataBaseManager()
    db_success = dbm.add_user(username, first_name, last_name, email, stored_pwd)

    if db_success:
        session['user'] = username
        session['authorized'] = True

        return redirect(url_for('render_gallery'))
    else:
        # Getting here means that either there was a database  error or the username is already taken
        # since the user will have to retry anyways, we might as well say there was an error with the
        # chosen username
        err_msg = ["Username is unavailable."]
        return render_template("newuser.html", error=err_msg, username=username, first_name=first_name,
                               last_name=last_name, email=email, password=password, password_conf=password_conf)


def compose_error_message(username, first_name, last_name, email, password, password_conf):
    err_msg = []

    if not username:
        err_msg.append("Invalid username.")

    if not first_name:
        err_msg.append("Invalid first name.")

    if not last_name:
        err_msg.append("Invalid last name.")

    if not email:
        err_msg.append("Invalid email.")

    if not password:
        err_msg.append("Invalid password.")

    if not password_conf:
        err_msg.append("Password and verification do not match.")

    if len(err_msg) > 0:
        err_msg.append("Please hover your cursor over the fields below to check their requirements.")
    else:
        err_msg = None

    return err_msg
