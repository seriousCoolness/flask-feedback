from models import User, db
from app import app
from secret import email

app.app_context().push()
db.drop_all()
db.create_all()

User.query.delete()

row_1 = User(username='caldw3ll', password='dev', email=email, first_name='Robert', last_name='Wyatt')

db.session.add(row_1)

db.session.commit()