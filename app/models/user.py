from . import db

class User(db.Model):
    __tablename__  = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return "<User %r>" % self.username