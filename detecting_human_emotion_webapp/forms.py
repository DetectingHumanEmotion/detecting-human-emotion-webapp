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

class UserInfoForm(FlaskForm):

    first_name = StringField(
        "First Name",
        default="",
        render_kw={
            "placeholder": "John"
        }
    )
    last_name = StringField(
        "Last Name",
        default="",
        render_kw={
            "placeholder": "Doe"
        }
    )

    race = StringField(
        "Race",
        default="",
        render_kw={
            "placeholder": "hispanic"
        }
    )
    gender = StringField(
        "Gender",
        default="",
        render_kw={
            "placeholder": "Male"
        }
    )
    age = IntegerField(
        "Age",

        render_kw={
            "placeholder": "22"
        }
    )
