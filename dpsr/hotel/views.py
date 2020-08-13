from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dpsr import  db
from dpsr.models import Hotel , Hoteldate
from sqlalchemy import desc,asc

hotels = Blueprint('hotels', __name__)

@hotels.route('/allhotel' , methods = ['GET' , 'POST'])
@login_required
def all_hotel():
    hotel = Hotel.query.order_by(Hotel.total_rooms.desc())
    return render_template('all_hotel.htm' , hotel = hotel)

@hotels.route('/<hotel_id>/allhotel' , methods = ['GET' , 'POST'])
@login_required
def single_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    return render_template('single_hotel.htm' , hotel = hotel)

@hotels.route('/<hotel_id>/<start_date>/<end_date>/book_hotel' , methods = ['GET' , 'POST'])
@login_required
def book_hotel(hotel_id , start_date, end_date):
    hotel = Hotel.query.get(hotel_id)
    current_user.hotel.append(hotel)
    date = Hoteldate(start_date = start_date,
                    end_date = end_date,
                    userid = current_user.id,
                    hotelid = hotel_id)
    db.session.add(date)
    db.session.commit()
    return redirect(url_for('hotels.all_hotel'))
