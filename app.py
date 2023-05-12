from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm

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
    if session.get('username'):
        return redirect(f"/users/{session['username']}")
    else:
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
        if User.query.filter_by(username=username).count():
            return render_template('login.html', form=form)

        password = form.password.data

        user=User.authenticate(username, password)
        if not user:
            return render_template('login.html', form=form)
        session['username'] = user.username

        return redirect(f'/users/{user.username}')
    else:
        return render_template('login.html', form=form)
    

@app.route('/logout')
def logout():
    if session.get('username'):
        session.clear()
        return redirect('/')
    else:
        return redirect('/login')
        

@app.route('/users/<username>')
def user_page(username):
    if username == session['username']:
        user=User.query.get_or_404(username)
        feedbacks=Feedback.query.filter_by(username=username)
        return render_template('user_profile.html', user=user,feedbacks=feedbacks)
    else:
        return redirect('/login')
    
@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if session['username'] == username:
        Feedback.query.filter_by(username=username).delete()
        User.query.filter_by(username=username).delete()
        db.session.commit()
        session.clear()
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=["GET","POST"])
def add_feedback(username):
    if session['username'] == username:
        form=FeedbackForm()

        if form.validate_on_submit():
            title=form.title.data
            content=form.content.data
            
            feedback=Feedback(title=title, content=content, username=username)

            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{feedback.username}')
        else:
            return render_template('feedback_add.html', username=username, form=form)
    else:
        redirect('/')

@app.route('/feedback/<int:id>/update', methods=["GET","POST"])
def edit_feedback(id):
    """edit existing feedback"""
    feedback=Feedback.query.get_or_404(id)
    if session['username'] == feedback.username:
        form=FeedbackForm()

        if form.validate_on_submit():
            feedback.title=form.title.data
            feedback.content=form.content.data
        
            db.session.commit()
            return redirect(f'/feedback/{id}')
        else:
            return render_template('feedback_edit.html', id=id, form=form)
    else:
        redirect('/')

@app.route('/feedback/<int:id>/delete', methods=["POST"])
def delete_feedback(id):
    feedback=Feedback.query.get_or_404(id)
    if session['username'] == feedback.username:
        users_name = feedback.username
        Feedback.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(f'/users/{users_name}')
    else:
        redirect('/')