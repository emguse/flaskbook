import logging
import os

from email_validator import validate_email, EmailNotValidError
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_mail import Mail, Message

# from flask_debugtoolbar import DebugToolbarExtension
# flask_debugtoolbar is not yet compatible with Flask 3.0.

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")
app.logger.setLevel(logging.DEBUG)
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# toolbar = DebugToolbarExtension(app)
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
mail = Mail(app)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/hello/<string:name>", methods=["GET", "POST"], endpoint="hello-endpoint")
def hello(name):
    return f"Hello, {name}!"


@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]
        error = False

        if not username:
            error = True
            flash("Username is required.")

        if not email:
            error = True
            flash("Email address is required.")

        if not description:
            error = True
            flash("Details is required.")

        try:
            validate_email(email)
        except EmailNotValidError:
            error = True
            flash("Email address format is invalid.")

        if error:
            flash("Please review your input.")
            return redirect(url_for("contact"))
        else:
            send_email(
                email,
                "Thank you for contacting us!",
                "contact_mail",
                username=username,
                description=description,
            )
            flash("Your inquiry has been submitted.")
            return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")


def send_email(to: str, subject: str, template: str, **kwargs):
    """Send message funcfion
    to: "Mail to"
    subject: "Mail subject"
    template: "Mail template"
    """
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
