from config import db


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    keywords = db.Column(db.String(255))
    lat = db.Column(db.String(18))
    lng = db.Column(db.String(18))
    city = db.Column(db.String(30))

    def __repr__(self):
        return '<Shop %r>' % self.name

    def __str__(self):
        return self.name
