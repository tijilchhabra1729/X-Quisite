from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
import os
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dpsr import  db
from dotenv import load_dotenv
from dpsr.models import Hotel , Hoteldate

tours = Blueprint('tours', __name__)

load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')

@tours.route('/vc', methods=['GET','POST'])
@login_required
def vc():
    return render_template('vc.html' )


@tours.route('/vc_login', methods=['POST'])
@login_required
def vc_login():
    username = request.get_json(force=True).get('username')
    if not username:
        abort(401)

    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room='My Room'))

    return {'token': token.to_jwt().decode()}
