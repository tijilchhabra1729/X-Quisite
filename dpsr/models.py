from datetime import datetime
from dpsr import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
hotel_user = db.Table('hotel_user',
  db.Column('user_id', db.Integer , db.ForeignKey('users.id')),
  db.Column('hotel_id', db.Integer , db.ForeignKey('hotel.id')))
class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    fname = db.Column(db.String(64))
    profile_image = db.Column(db.String(64), nullable = False, default = 'Site_icon.png')
    email = db.Column(db.String(64),unique = True,index = True)
    username = db.Column(db.String(64),unique = True,index = True)
    password_hash = db.Column(db.String(128))

    car = db.relationship('Car' , backref = 'user' , lazy = 'dynamic')
    hotel = db.relationship('Hotel' , secondary = hotel_user , backref = db.backref('user', lazy = 'dynamic'))
    question = db.relationship('Question' , backref = 'user' , lazy = 'dynamic')
    answer = db.relationship('Answer' , backref = 'user' , lazy = 'dynamic')
    likes = db.relationship('Like' , backref = 'user' , lazy = 'dynamic')
    unlikes = db.relationship('Unlike' , backref = 'user' , lazy = 'dynamic')

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
    car_image = db.Column(db.String(64), nullable = False)
    available = db.Column(db.String , default = 'Yes')
    driver = db.Column(db.String)

    userid = db.Column(db.Integer , db.ForeignKey('users.id'))

    def __init__(self, name ,seats ,price ,userid ,driver , car_image):
        self.name = name
        self.seats = seats
        self.price = price
        self.driver = driver
        self.userid = userid
        self.car_image = car_image

class Question(db.Model , UserMixin):
    __tablename__ = 'questions'

    id = db.Column(db.Integer , primary_key = True)
    question = db.Column(db.String)
    date = db.Column(db.DateTime,nullable = False,default=datetime.now)

    userid = db.Column(db.Integer , db.ForeignKey('users.id'))
    answer = db.relationship('Answer' , backref = 'question' , lazy = 'dynamic')
    def __init__(self,question,userid):
        self.question = question
        self.userid = userid

class Answer(db.Model , UserMixin):
    __tablename__ = 'answers'
    id = db.Column(db.Integer , primary_key = True)
    answer = db.Column(db.String)
    like = db.Column(db.Integer , default = 0)
    unlike = db.Column(db.Integer , default = 0)
    date = db.Column(db.DateTime,nullable = False,default=datetime.now)

    questionid = db.Column(db.Integer , db.ForeignKey('questions.id'))
    userid = db.Column(db.Integer , db.ForeignKey('users.id'))
    likes = db.relationship('Like' , backref = 'answer' , lazy = 'dynamic')
    unlikes = db.relationship('Unlike' , backref = 'answer' , lazy = 'dynamic')

    def __init__(self,answer,questionid,userid):
        self.answer = answer
        self.questionid = questionid
        self.userid = userid

class Like(db.Model , UserMixin):
    __tablename__ = 'likes'
    id = db.Column(db.Integer , primary_key = True)

    answerid = db.Column(db.Integer , db.ForeignKey('answers.id'))
    userid = db.Column(db.Integer , db.ForeignKey('users.id'))

    def __init__(self,answerid,userid):
        self.answerid = answerid
        self.userid = userid

class Unlike(db.Model , UserMixin):
    __tablename__ = 'unlikes'
    id = db.Column(db.Integer , primary_key = True)

    answerid = db.Column(db.Integer , db.ForeignKey('answers.id'))
    userid = db.Column(db.Integer , db.ForeignKey('users.id'))

    def __init__(self,answerid,userid):
        self.answerid = answerid
        self.userid = userid

class Hotel(db.Model , UserMixin):
    __tablename__ = 'hotel'

    id = db.Column(db.Integer , primary_key = 'True')
    name = db.Column(db.Integer)
    total_rooms = db.Column(db.Integer)
    available_rooms = db.Column(db.Integer)
    picture = db.Column(db.String)
    pool = db.Column(db.String)
    restaurant = db.Column(db.String)
    other = db.Column(db.String)
    location = db.Column(db.String)
    description = db.Column(db.String)
    def __init__(self, name , total_rooms , available_rooms , pool , restaurant , other , location , picture , description):
        self.name = name
        self.total_rooms = total_rooms
        self.available_rooms = available_rooms
        self.pool = pool
        self.restaurant = restaurant
        self.other = other
        self.location = location
        self.picture = picture
        self.description = description
