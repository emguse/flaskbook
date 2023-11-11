from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField


class UploadImageForm(FlaskForm):
    image = FileField(
        validators=[
            FileRequired("Please specify the image file."),
            FileAllowed(["png", "jpg", "jpeg"], "Unsupported image format."),
        ]
    )
    submit = SubmitField("UPLOAD")
