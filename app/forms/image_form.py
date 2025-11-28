from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired

from app.api.upload_helper import ALLOWED_EXTENSIONS


class ImageForm(FlaskForm):
    image = FileField(
        "image",
        validators=[FileRequired(), FileAllowed(list(ALLOWED_EXTENSIONS))],
    )
