import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)
Migrate(app,db)



login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

from dpsr.users.views import users
from dpsr.home.views import home
from dpsr.car.views import cars
from dpsr.hotel.views import hotels
from dpsr.faq.views import faqs
from dpsr.tours.views import tours

app.register_blueprint(faqs)
app.register_blueprint(home)
app.register_blueprint(users)
app.register_blueprint(cars)
app.register_blueprint(hotels)
app.register_blueprint(tours)
