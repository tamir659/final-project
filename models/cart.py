from db import db 
class Cart(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) 
    deliveries = db.relationship('Delivery',backref='cart',uselist=False)
    items = db.relationship('Items',backref = 'cart') 