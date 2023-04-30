from db import db 
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    first_name = db.Column(db.String(200),nullable=False)
    last_name = db.Column(db.String(200),nullable=False)
    is_staff = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    deliveries = db.relationship('Delivery',backref ='user') 