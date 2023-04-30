from flask import request 
from models.user import User 

def auth():
    username= request.cookies.get('username')
    user = User.query.filter_by(username=username).first()
    if user!= None:
        return True
    else:
        return False

def is_staff_auth():
    username= request.cookies.get('username')
    user = User.query.filter_by(username=username).first()
    if user.is_staff == 'True':
        return True
    else:
        return False