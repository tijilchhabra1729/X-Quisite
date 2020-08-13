from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField ,IntegerField , RadioField , FileField
from wtforms.validators import DataRequired, Email , EqualTo, Length
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user


class MakeCarForm(FlaskForm):
    name = StringField('What is the name of your car' , validators=[DataRequired()])
    seats = IntegerField('How many seats does your car have' , validators=[DataRequired()])
    price = IntegerField('What is the price of your car' , validators=[DataRequired()])
    picture = FileField('A picture of your car please' , validators=[DataRequired()])
    driver = RadioField('Does your car come with a driver' , choices=[('Yes','It Does'),('No','It does not')])
    submit = SubmitField('Let people see')

class UpdateCarForm(FlaskForm):
    name = StringField('What is the name of your car' , validators=[DataRequired()])
    seats = IntegerField('How many seats does your car have' , validators=[DataRequired()])
    price = IntegerField('What is the price of your car' , validators=[DataRequired()])
    picture = FileField('A picture of your car please')
    driver = RadioField('Does your car come with a driver' , choices=[('Yes','It Does'),('No','It does not')] , validators=[DataRequired()])
    available = RadioField('Is your car available' , choices=[('Yes','Yes'),('No','No')])
    submit = SubmitField('Update')

class SearchCarForm(FlaskForm):
    seats = IntegerField('How many seats' )
    driver = RadioField('Do you want car with driver' , choices=[('Yes','Yes'),('No','No')]  )
    submit = SubmitField('Filter')
