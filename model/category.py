from config import db
from model.table import Post


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    shops = db.relationship('Shop', backref=db.backref('category', lazy='select'))

    def __repr__(self):
        return '<Category %r>' % self.name
    
    def __str__(self):
        return self.name
