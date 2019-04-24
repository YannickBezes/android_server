from config import db
from model.table import Post


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    public = db.Column(db.Boolean)

    posts = db.relationship('Post')

    def __repr__(self):
        return '<Group %r>' % self.name
    
    def __str__(self):
        return self.name

