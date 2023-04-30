from db import db 
class Dish(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False,unique=True)
    price = db.Column(db.Integer,nullable=False)
    description = db.Column(db.Text,nullable=False)
    image = db.Column(db.String(200),nullable=False)
    is_gluten_free = db.Column(db.String(200),nullable=False)
    is_vegeterian = db.Column(db.String(200),nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    item = db.relationship('Items',backref = 'dish')