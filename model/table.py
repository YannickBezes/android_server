from config import db

subs = db.Table('subs',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

sub_requests = db.Table('sub_requests', 
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Post(db.Model):
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    date = db.Column(db.String(16), primary_key=True) # Format 'dd/mm/yyyy-hh:mm'
    content = db.Column(db.String(280))
    user = db.relationship('User')