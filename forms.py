from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Email
class RegisterUserForm(FlaskForm):
    """A form for adding users."""

    username = StringField('Username', validators=[InputRequired(), Length(max=20)])

    password = PasswordField('Password', validators=[InputRequired()])

    email = EmailField('Email', validators=[InputRequired(), Email(), Length(max=50)])

    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])

    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])
    
class LoginUserForm(FlaskForm):
    """A form for authenticating existing users."""

    username = StringField('Username', validators=[InputRequired(), Length(max=20)])

    password = PasswordField('Password', validators=[InputRequired()])