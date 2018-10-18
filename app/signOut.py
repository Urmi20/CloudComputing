from flask import render_template, session
from app import webapp


@webapp.route('/sign_out', methods=['GET'])
def sign_out():
    session.clear()

    return render_template('index.html')
