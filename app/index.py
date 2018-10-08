from flask import render_template, Flask, redirect, url_for,request
from flask import g as user_data
from app import webapp
from os import urandom
import mysql.connector as conn

webapp.secret_key = urandom(24)

@webapp.route("/")
def index():
    if user_data.authorized is True:
        return redirect(url_for("welcome"))

    return render_template("index.html")

@webapp.route("/new_user")
def new_user():
    return render_template("newuser.html")

@webapp.route('/newuser',methods=['POST'])
def newuser():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    username = request.form.get('uname')
    email = request.form.get('email')
    password = request.form.get('pswd')

    #dbs=conn.connect(user="root",password="root@1234",host="127.0.0.1",database="CloudComputing",auth_plugin="mysql_native_password")
    #cnx=dbs.cursor()
    #cnx.execute("Database Management/createDB.sql")
    #cnx.close()
    return render_template("index.html")