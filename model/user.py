from config import db
from model.table import subs, Post

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    gender = db.Column(db.String(6))
    height = db.Column(db.Float())
    weight = db.Column(db.Float())
    lat = db.Column(db.String(18))
    lng = db.Column(db.String(18))
    city = db.Column(db.String(30))
    last_searches = db.Column(db.String(255))
    interest = db.Column(db.Text())

    subscriptions = db.relationship('Group', secondary=subs, backref=db.backref('subscribers', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.username
    
    def __str__(self):
        return "{} {}, {}".format(self.firstname, self.lastname, self.username)


