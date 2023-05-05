
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models import User



class SearchForm(FlaskForm):
    search_name = StringField('Name of movie or TV seria',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Search')


class UpcomingForm(FlaskForm):
    number_of_movies = IntegerField('Number of movies to show',
                           validators=[DataRequired(), NumberRange(min=1, max=50)])
    submit = SubmitField('Search')

