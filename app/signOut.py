from flask import render_template, session
from app import userUI
from management import managerUI


@userUI.route('/sign_out', methods=['GET'])
def sign_out():
    session.clear()

    return render_template('index.html', type="user")

@managerUI.route('/sign_out', methods=['GET'])
def sign_out():
    session.clear()

    return render_template('index.html', type="manager")
