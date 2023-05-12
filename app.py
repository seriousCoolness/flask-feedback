from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
from forms import RegisterUserForm, LoginUserForm

app = Flask(__name__)

DATABASE_NAME = 'feedback'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
app.app_context().push()

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

        session['username'] = user.username

        return redirect(f'/users/{user.username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=["GET","POST"])
def login_page():

    form=LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user=User.authenticate(username, password)

        session['username'] = user.username

        return redirect(f'/users/{user.username}')
    else:
        return render_template('login.html', form=form)
    

@app.route('/logout')
def logout():
    if session['username']:
        session.clear()
        return redirect('/')
    else:
        return redirect('/login')
        

@app.route('/users/<username>')
def user_page(username):
    if username == session['username']:
        return render_template('user_profile.html', user=User.query.get_or_404(username))
    else:
        return redirect('/login')
