from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, length


class UserForm(FlaskForm):
    username: str = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required."),
            length(max=30, message="Please enter within 30 characters."),
        ],
    )
    email: str = StringField(
        "Email address",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Must be in email address format."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
        ],
    )
    submit = SubmitField("Register")
