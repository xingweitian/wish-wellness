from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from main import db, app


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def password(self):
        raise AttributeError("Error, password is a write only attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


if __name__ == "__main__":
    with app.app_context():
        u = User(username='admin@gmail.com', password='admin')
        db.session.add(u)
        db.session.commit()
