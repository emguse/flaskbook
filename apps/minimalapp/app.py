from email_validator import validate_email, EmailNotValidError
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

app = Flask(__name__)

app.config["SECRET_KEY"] = "7uT64T6WJlrzxuAKNCnk4u5gpSe8CGbM"


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
            flash("Your inquiry has been submitted.")
            return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")
