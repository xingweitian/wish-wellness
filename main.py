from flask import Flask, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.init_app(app)

CORS(app)


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify('pong!')


def init():
    from views.auth import auth
    from views.user import user
    app.register_blueprint(blueprint=auth, url_prefix='/auth')
    app.register_blueprint(blueprint=user, url_prefix='/user')


@login_manager.user_loader
def load_user(id):
    from model import User
    return User.query.get(int(id))


if __name__ == '__main__':
    init()
    app.run(app.config['ADDRESS'], app.config['PORT'], app.config['DEBUG'])
