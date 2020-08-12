from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField , TextAreaField
from wtforms.validators import DataRequired, Email , EqualTo, Length
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed


class SearchQForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('search')

class MakeQForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    submit = SubmitField('Post Question')

class MakeAForm(FlaskForm):
    answer = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Post Answer')
