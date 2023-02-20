from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect credentials, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('first-name')
        lastName = request.form.get('last-name')
        passwordNew = request.form.get('password-new')
        passwordConfirm = request.form.get('password-confirm')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(firstName) < 1:
            flash('Please enter a first name', category='error')
        elif len(lastName) < 1:
            flash('Please enter a last name', category='error')
        elif len(passwordNew) < 8:
            flash('Password must be at least 8 characters', category='error')
        elif passwordNew != passwordConfirm:
            flash('Passwords must match', category='error')
        else:
            new_user = User(email=email, first_name=firstName, last_name=lastName)
            new_user.set_password(passwordNew)
            db.session.add(new_user)
            db.session.commit()
            flash('Account successfully created!', category='success')
            login_user(new_user, remember=True)
            #redirects user to home page
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
