from flask import render_template, request
from app import webapp
from app.tools.email import Email


# TODO: Have a class to hold all the constants
@webapp.route("/forgotpwd")
def forgotpwd():
    return render_template("forgotpwd.html")


@webapp.route("/recovery_submit", methods=["POST"])
def recovery_submit():
    recipient = request.form.get("email")

    email = Email("smtp.gmail.com", 587, "ece1779.project.fall.2018", "aSd123qWe456zxc")
    email.send("ece1779.project.fall.2018@gmail.com", recipient, "InstaKilo Password Recovery",
               "Here is your link to change your password")

    return render_template("index.html")