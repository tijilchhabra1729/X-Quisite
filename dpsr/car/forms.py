from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField ,IntegerField , RadioField
from wtforms.validators import DataRequired, Email , EqualTo, Length
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user


class MakeCarForm(FlaskForm):
    name = StringField('What is the name of your car' , validators=[DataRequired()])
    seats = IntegerField('How many seats does your car have' , validators=[DataRequired()])
    price = IntegerField('What is the price of your car' , validators=[DataRequired()])
    driver = RadioField('Does your car come with a driver' , choices=[('Yes','It Does'),('No','It does not')])
    submit = SubmitField('Let people see')
