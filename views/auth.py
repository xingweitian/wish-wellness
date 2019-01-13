from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required
from model import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(username=email).first()
    if user is not None and user.verify_password(password):
        login_user(user)
        return jsonify('100')
    else:
        return jsonify('200')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify('100')
