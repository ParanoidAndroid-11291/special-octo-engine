from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template('home.html', user=current_user, formatTime=formatTime)

def formatTime(date):
    return date.strftime('%B %d %Y - %I:%M %p')

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note_to_delete = Note.query.get(noteId)
    if note:
        if note_to_delete.user_id == current_user.id:
            db.session.delete(note_to_delete)
            db.session.commit()

    return jsonify({})

@views.route('/settings')
@login_required
def settings():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('first-name')
        lastName = request.form.get('last-name')
        passwordCurrent = request.form.get('password-current')
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

    return render_template('settings.html', user=current_user)
