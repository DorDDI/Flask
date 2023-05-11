
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models import User



class SearchForm(FlaskForm):
    search_name = StringField('Name of movie or TV seria',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Search')


class UpcomingForm(FlaskForm):
    number_of_movies = IntegerField('Number of movies to show', default=1,
                           validators=[DataRequired(), NumberRange(min=1, max=50)])
    submit = SubmitField('Search')

class PopularForm(FlaskForm):
    number_of_movies = IntegerField('Number of movies to show', default=1,
                                    validators=[DataRequired(), NumberRange(min=1, max=50)])
    start = IntegerField('From which index to start', default=1,
                                    validators=[DataRequired(), NumberRange(min=1)])
    choices = SelectField('Choose genre', choices=["All", "Action", "Adventure", "Animation", "Biography", "Comedy",
                                                   "Crime", "Documentary", "Drama", "Family", "Fantasy", "Game-Show",
                                                   "History", "Horror", "Music", "Musical", "Mystery", "News",
                                                   "Reality-TV", "Romance", "Sci-Fi", "Short", "Sport", "Talk-Show",
                                                   "Thriller", "War", "Western"], validators=[DataRequired()])
    submit = SubmitField('Search')


class WatchlistForm(FlaskForm):
    rate = SelectField('Your rate', choices=["No Rate","1 - Trash", "2 - Horrible", "3 - Very bad", "4 - Bad", "5 - Average",
                                             "6 - OK", "7 - Good", "8 - Very good", "9 - Excellent",
                                             "10 - Brilliant "], validators=[DataRequired()])
    watch_type = SelectField('What are you now', choices=["Watching", "On hold", "On the list", "Complete"],
                             validators=[DataRequired()])
    submit = SubmitField('Submit')

