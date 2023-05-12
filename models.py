from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """The table containing encryted login shit."""

    __tablename__ = "users"

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).all()

    def __repr__(self):
        p = self
        return f'<User id={p.id} name={p.name} value={p.value}>'


    username = db.Column(db.String(20),
                   unique=True,
                   primary_key=True)
    
    password = db.Column(db.Text,
                     nullable=False)
    
    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)
    
    first_name = db.Column(db.String(30),
                           nullable=False)
    
    last_name = db.Column(db.String(30),
                          nullable=False)
    
    @classmethod
    def register(cls, username, pwd):

        hashed=bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")


        return cls(username=username, password=hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """
        checks username, and makes sure pass-hash matches the pass word, word dawg
        """


        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):

            return u
        else:
            return False