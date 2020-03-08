from bot import db
from flask_sqlalchemy import SQLAlchemy

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)

    def __repr__(self):
        return "<question={self.question} answer={self.answer}>".format(self=self)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text)
    status = db.Column(db.Text)

    def __repr__(self):
        return "<user_id={self.user_id} status={self.status}>".format(self=self)

def init():
    db.create_all()

