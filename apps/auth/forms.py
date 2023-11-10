from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SignUpForm(FlaskForm):
    username: str = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required."),
            Length(min=1, max=30, message="Please enter within 30 characters."),
        ],
    )
    email: str = StringField(
        "Email address",
        validators=[
            DataRequired(message="Email address is required."),
            Email(message="Must be in email address format."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
        ],
    )
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    email: str = StringField(
        "Email address",
        validators=[
            DataRequired("Email address is required."),
            Email("Must be in email address format."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired("Password is required.")],
    )
    submit = SubmitField("Login")
