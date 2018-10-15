from flask import render_template, request, session, redirect, url_for
from app import webapp
from app.tools.email import Email
from app.tools.dbTools import DataBaseManager
import re

# TODO: Have a class to hold all the constants
@webapp.route("/forgotpwd")
def forgotpwd():
    if 'authorized' in session and session['authorized'] is True:
        return redirect(url_for("welcome"))

    else:
        return render_template("forgotpwd.html")


@webapp.route("/recovery_submit", methods=["POST"])
def recovery_submit():
    recipient = request.form.get("email")
    dbm = DataBaseManager()
    email_success = dbm.email_already_exists(recipient)

    if email_success:

        token = DataBaseManager.get_token()
        user = email_success
        email = Email("smtp.gmail.com", 587, "ece1779.project.fall.2018", "aSd123qWe456zxc")
        email.send("ece1779.project.fall.2018@gmail.com", recipient, "Password Recovery",
                   f'''Hi {user},\n\n
                       visit the following link to reset your password - 
                       {url_for('reset_token', token=token, _external=True)}''')

        return render_template("index.html")
    else:
        email_not_reg = True
        return render_template("forgotpwd.html", error_value=email_not_reg)


@webapp.route("/recovery_submit/<token>")
def reset_token(token):
    if 'authorized' in session and session['authorized'] is True:
        return redirect(url_for("welcome"))
    user = DataBaseManager.verify_token(token)
    if user is None:
        return render_template("NewPwd.html", error=True)
    return render_template("NewPwd.html", error=False)
