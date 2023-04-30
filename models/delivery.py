from db import db 
class Delivery(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    is_delivered = db.Column(db.String(200),nullable=False)
    adress = db.Column(db.String(200),nullable=False)
    comment = db.Column(db.String(200),nullable=False)
    created = db.Column(db.DateTime)
    total_price = db.Column(db.Integer,nullable=False) 
    cart_id = db.Column(db.Integer,db.ForeignKey('cart.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))