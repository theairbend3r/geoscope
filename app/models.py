from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.Integer)
    age = db.Column(db.Integer)
    med_cond = db.Column(db.Text(30))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    pin_code = db.Column(db.Integer)
    face_encoding = db.Column(db.Text(500))

    def __repr__(self):
        return '<Users {}>'.format(self.first_name)
