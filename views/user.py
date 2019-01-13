import json

from flask import Blueprint, jsonify, request
from flask_login import login_required

from model import User
from main import db
from mongo_transaction import MongoTransaction

from tone_analyzer import tone

user = Blueprint('user', __name__)
m = MongoTransaction()


@user.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    age = request.form['age']
    gender = request.form['gender']
    interests = request.form['interests']
    _medications = request.form['medications']
    medications = _medications.split(",")
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    user = User(username=email, password=password)
    db.session.add(user)
    db.session.commit()
    m.insert(email, age, gender, interests, medications, first_name, last_name)
    return jsonify('100')


@user.route('/<username>', methods=['GET'])
@login_required
def user_info(username):
    res = str(m.search(username))
    return jsonify(res)


@user.route('/survey', methods=['POST'])
def survey():
    email = request.form['email']
    anxiety = int(request.form['anxiety'])
    mood = int(request.form['mood'])
    eating = int(request.form['eating'])
    psych = int(request.form['psych'])
    pers = int(request.form['pers'])
    score = anxiety + mood + eating + psych + pers
    res = m.survey(email, anxiety, mood, eating, psych, pers)
    if res:
        return jsonify(score)
    else:
        return jsonify('200')


@user.route('/survey_data', methods=['POST'])
def survey_data():
    email = request.form['email']
    res = m.search_survey_data(email)
    r = str(res)
    print(r)
    return json.dumps(r)


@user.route('/medications', methods=['POST'])
def medications():
    email = request.form['email']
    _data = m.search(email)
    if _data:
        medications = _data['medication']
    else:
        medications = None
    res = dict()
    res['medications'] = medications
    print(res)
    return jsonify(res)


@user.route('get_username', methods=['POST'])
def get_username():
    email = request.form['email']
    _data = m.search(email)
    if _data:
        first_name = _data['first_name']
    else:
        first_name = None
    print(first_name)
    return first_name


@user.route('/tone', methods=['POST'])
def tone_analyzer():
    sentence = request.form['sentence']
    _data = tone(sentence)
    res = []
    if isinstance(_data, str):
        _data = json.loads(_data)
    if 'sentences_tone' in _data.keys():
        _tones = _data['sentences_tone']
        for each in _tones:
            res.append(each['tones'][0]['tone_name'] + ":" + each['text'])
    else:
        _tones = _data['document_tone']['tones']
        for each in _tones:
            res.append(each['tone_name'] + ":" + "no sentences")
    return str(res)
