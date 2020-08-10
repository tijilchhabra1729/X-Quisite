from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dpsr import  db
from dpsr.models import User
from dpsr.users.forms import RegistrationForm,LoginForm
from dpsr.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.index"))

@users.route('/register' , methods = ['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(fname = form.fname.data, email=form.email.data,
                    username = form.username.data,
                    password= form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration')
        return redirect(url_for('users.login'))

    return render_template('register.htm', form = form)

@users.route('/login',methods=['GET','POST'])
def login():
    error = ''
    if current_user.is_authenticated == False:
        form = LoginForm()
        if form.validate_on_submit():

            user = User.query.filter_by(email=form.email.data).first()

            if user is not None and user.check_password(form.password.data) :

                login_user(user)
                flash('Log in Success!')

                next = request.args.get('next')
                if next == None or not next[0] =='/':
                    next = url_for('home.index')
                return redirect(next)
            elif user is not None and user.check_password(form.password.data) == False:
                error = 'Wrong Password'
            elif user is None:
                error = 'No such login Pls create one'
        return render_template('login.htm', form=form, error = error)
    else:
        return render_template('login_logout.htm')
