# core/views.py
from dpsr.models import User
from flask import Blueprint,render_template,request, url_for
from flask_login import current_user

home = Blueprint('home',__name__)

@home.route('/')
def index():
    return render_template('index.htm')
