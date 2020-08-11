from datetime import datetime
from dpsr import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    fname = db.Column(db.String(64))
    profile_image = db.Column(db.String(64), nullable = False, default = 'Site_icon.png')
    email = db.Column(db.String(64),unique = True,index = True)
    username = db.Column(db.String(64),unique = True,index = True)
    password_hash = db.Column(db.String(128))

    car = db.relationship('Car' , backref = 'user' , lazy = 'dynamic')

    def __init__(self, fname, email, username, password):
        self.email = email
        self.fname =fname
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Car(db.Model , UserMixin):
    __tablename__ = 'cars'

    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String)
    seats = db.Column(db.Integer)
    price = db.Column(db.Integer)
    available = db.Column(db.String , default = 'No')
    driver = db.Column(db.String)

    userid = db.Column(db.Integer , db.ForeignKey('users.id'))

    def __init__(self, name ,seats ,price ,userid ,driver):
        self.name = name
        self.seats = seats
        self.price = price
        self.driver = driver
        self.userid = userid
