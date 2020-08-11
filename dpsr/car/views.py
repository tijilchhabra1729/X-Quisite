from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dpsr import  db
from dpsr.models import User , Car
from dpsr.car.forms import MakeCarForm
from sqlalchemy import asc

cars = Blueprint('cars', __name__)

@cars.route('/makeit' , methods = ['GET' , 'POST'])
@login_required
def make_car():
    form = MakeCarForm()
    if form.validate_on_submit():
        car = Car(name = form.name.data,
                  seats = form.seats.data,
                  price = form.price.data,
                  driver = form.driver.data,
                  userid = current_user.id)
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('cars.show_car'))
    return render_template('car.htm' , form = form)


@cars.route('/showit' , methods = ['GET' , 'POST'])
@login_required
def show_car():
    car = []
    cars = Car.query.order_by(Car.seats.asc())
    for c in cars:
        car.append(c)
    return render_template('all_car.htm' , car = car)
