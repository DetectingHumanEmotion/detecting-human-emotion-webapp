from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    RadioField,
    SelectField,
    SubmitField,
    TextAreaField,
    IntegerField,
)
from wtforms.validators import DataRequired

class UserInfoForm(FlaskForm):

    first_name = StringField(
        "First Name",
        default="",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "John"
        }
    )
    last_name = StringField(
        "Last Name",
        default="",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Doe"
        }
    )

    race = StringField(
        "Race",
        default="",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "hispanic"
        }
    )
    gender = StringField(
        "Gender",
        default="",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Male"
        }
    )
    age = IntegerField(
        "Age",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "22"
        }
    )
