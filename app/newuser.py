from flask import render_template, request, redirect, url_for, session
from app import webapp
from app.tools import validate
import mysql.connector
from mysql.connector import errorcode


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
        return render_template("newuser.html", error=err_msg, username=username, first_name=first_name, last_name=last_name,
                               email=email, password=password, password_conf=password_conf)

    try:
        cnx = mysql.connector.connect(user="root", password="password", host="127.0.0.1", database="InstaKilo")

        query = ('insert into users (id, profile, name, first_name, last_name, email, pw_salt_hash) values (DEFAULT, (select id from user_profiles where type = "user"), %s, %s, %s, %s, %s)')

        cursor = cnx.cursor()
        cursor.execute(query, (username, first_name, last_name, email, password))

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cnx.commit()
    cursor.close()
    cnx.close()
    session['user'] = username
    session['authorized'] = True

    return redirect(url_for('welcome'))


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
        err_msg.append("Please check the requirements for the fields listed above and try again.")
    else:
        err_msg = None

    return err_msg
