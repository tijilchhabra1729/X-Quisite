from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dpsr import  db
from dpsr.models import User , Car
from dpsr.car.forms import MakeCarForm , UpdateCarForm , SearchCarForm
from sqlalchemy import asc , desc
from dpsr.car.picture_handler import add_car_pic
import stripe

cars = Blueprint('cars', __name__)

public_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

@cars.route('/makeit' , methods = ['GET' , 'POST'])
@login_required
def make_car():
    form = MakeCarForm()
    if form.validate_on_submit():
        id = current_user.id
        pic = add_car_pic(form.picture.data,id)
        car = Car(name = form.name.data,
                  seats = form.seats.data,
                  price = form.price.data,
                  driver = form.driver.data,
                  userid = current_user.id,
                  car_image = pic)
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('cars.show_car'))
    return render_template('car.htm' , form = form)


@cars.route('/showit' , methods = ['GET' , 'POST'])
@login_required
def show_car():
    car = []
    cars = []
    form = SearchCarForm()
    if form.validate_on_submit():
        if form.driver.data and form.seats.data:
            cars = Car.query.order_by(Car.price.asc()).filter_by(available = 'Yes' , seats = form.seats.data , driver = form.driver.data)
            print(form.seats.data)
            print(form.driver.data)
        elif form.driver.data and form.seats.data is None:
            cars = Car.query.order_by(Car.price.asc()).filter_by(available = 'Yes' ,  driver = form.driver.data)
            print(form.driver.data)
        elif form.seats.data and form.driver.data is None:
            cars = Car.query.order_by(Car.price.asc()).filter_by(available = 'Yes' , seats = form.seats.data)
            print(form.seats.data)
        else:
            cars = Car.query.order_by(Car.price.asc()).filter_by(available = 'Yes')
    else:
        cars = Car.query.order_by(Car.price.asc()).filter_by(available = 'Yes')
    for c in cars:
        car.append(c)
    return render_template('all_car.htm' , car = car , form = form)

@cars.route('/<car_id>/detail' , methods = ['GET' , 'POST'])
@login_required
def single_car(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('single_car.htm', car = car)

@cars.route('/<car_id>/updatecar' ,methods = ['GET' , 'POST'])
@login_required
def updatecar(car_id):
    car = Car.query.get_or_404(car_id)
    form = UpdateCarForm()
    if car.user.id != current_user.id:
        abort(403)
    else:
        if form.validate_on_submit():
            car.name = form.name.data
            car.price = form.price.data
            car.seats = form.seats.data
            car.driver = form.driver.data
            car.available = form.available.data
            if form.picture.data:
                id = current_user.id
                pic = add_car_pic(form.picture.data,id)
                car.car_image = pic
            db.session.commit()
            return redirect(url_for('cars.show_car'))
        elif request.method == 'GET':
            form.name.data = car.name
            form.price.data = car.price
            form.seats.data = car.seats
            form.driver.data = car.driver
            form.available.data = car.available
    return render_template('updatecar.htm' , form = form , car_id = car_id)

@cars.route('/<car_id>/deletecar' , methods = ['GET','POST'])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if current_user != car.user:
        abort(403)
    else:
        db.session.delete(car)
        db.session.commit()
    return redirect(url_for('cars.show_car'))

########## PAYMENTS ##################

@cars.route('/<car_id>/index', methods=['GET','POST'])
def index(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('payment1.html', public_key=public_key, car=car)

@cars.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@cars.route('/payment', methods=['POST'])
def payment():

    # CUSTOMER INFORMATION
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # CHARGE/PAYMENT INFORMATION
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1999,
        currency='inr',
        description='Donation'
    )

    return redirect(url_for('cars.thankyou'))
#####################################################
