from config import db


class Pub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    keywords = db.Column(db.String(255))
    image = db.Column(db.String(255))

    def __repr__(self):
        return '<Pub %r>' % self.name
    
    def __str__(self):
        return self.name
