from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
from forms import RegisterUserForm

app = Flask(__name__)

DATABASE_NAME = 'database_name_here'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

@app.route('/')
def home_page():
    """Shows the home page."""
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_form():
    """Shows form for making user"""
    
    form=RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user=User.register(username,password)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        db.session.add(user)
        db.session.commit()

        return redirect('/secret')
    else:
        return render_template('register.html', form=form)
