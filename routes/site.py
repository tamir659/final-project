from flask import render_template,request,redirect,make_response,url_for,Blueprint
from db import db 
from datetime import datetime as dt 
from models.user import User
from models.items import Items
from models.category import Category
from models.dish import Dish
from models.cart import Cart
from models.delivery import Delivery  
from utils import is_staff_auth , auth  
from forms import Sign_up_Form , edit_category_form , edit_dish_form , add_category_form,add_dish_form 

site_bp = Blueprint('site',__name__) 
   
@site_bp.route('/') 
def main():
     if auth():
        return redirect('/categories')
     else:
        return render_template('site/main.html') 


@site_bp.route('/sign_up',methods=['GET','POST']) 
def sign_up():
        form = Sign_up_Form()
        if auth():
         return redirect('/categories')
        elif request.method == 'POST' and form.validate_on_submit():               
                new_user = User(username=form.username.data,
                                password=form.password.data,
                                first_name =form.first_name.data,
                                last_name=form.last_name.data,
                                is_staff=request.form['is_staff'],
                                email = form.email.data
                )
                first_name =form.first_name.data
                last_name=form.last_name.data
                if first_name.isalpha() and last_name.isalpha():
                    db.session.add(new_user)
                    db.session.commit()
                    new_cart = Cart( user_id = new_user.id)
                    db.session.add(new_cart)
                    db.session.commit()
                    return redirect('/log_in') 
                else:
                     return 'name or last name cant contain numbers'
        return render_template('site/sign_up.html',form=form)

@site_bp.route('/log_in',methods = ['GET','POST']) 
def log_in():
    if auth():
        return redirect('/categories')
    elif request.method == 'POST':
     user = User.query.filter_by(username=request.form['username']).first()
     if user != None:
         if user.password == request.form['password']:
             resp = make_response(redirect('/categories')) 
             resp.set_cookie('username',user.username) 
             return resp 
         else:
             return'password or username incorrect'
     else:
          return'account not found'
    return render_template('site/log_in.html')

@site_bp.route('/categories')
def categories():
    user = User.query.filter_by(username=request.cookies.get('username')).first()
    if auth():
        category = Category.query.all()
        return render_template('site/categories.html',category=category,user=user)
    else:
        return redirect('/') 

@site_bp.route('/show_category_dishes/<int:id>')
def show_category_dishes(id):
    if auth():
        category=Category.query.get(id) 
        return render_template('site/show_category_dishes.html',category=category) 
    else:
        return redirect('/')

@site_bp.route('/show_dish/<int:id>',methods=['GET','POST'])
def show_dish(id):
    if auth():
        dish=Dish.query.get(id)
        user = User.query.filter_by(username=request.cookies.get('username')).first()
        user_id = user.id
        cart = Cart.query.filter_by(user_id = user_id).first()
        cart_id= cart.id
        if request.method == 'POST': 
                if request.form['amount'] != '':
            
                    new_item = Items(
                            dish_id = id,
                            cart_id = cart_id,
                            amount = request.form['amount']
                        )
                    db.session.add(new_item)
                    db.session.commit()
                    return redirect('/categories')
                else:
                    redirect('/categories')
        return render_template('site/show_dish.html',dish=dish) 
    else:
        return redirect('/') 

@site_bp.route('/sign_out')
def sign_out():
    resp = make_response(redirect('/'))
    resp.delete_cookie('username')
    return resp 

@site_bp.route('/cart')
def cart():
    if auth():
        dish = Dish.query.all() 
        user = User.query.filter_by(username=request.cookies.get('username')).first() 
        user_id = user.id
        cart = Cart.query.filter_by(user_id = user_id).first()
        total_price = 0
        for item in cart.items:
                total_price+=(item.dish.price)*(item.amount) 
        return render_template('site/cart.html',cart=cart,dish=dish,total_price=total_price) 
    else:
        return redirect('/')
    
@site_bp.route('/remove_item/<int:id>',methods = ['GET','POST'])
def remove_item(id):
    if auth():
        item=Items.query.get(id) 
        if request.method == 'POST':
                    db.session.delete(item)
                    db.session.commit()
                    return redirect('/cart') 
        return render_template('site/remove_item.html',item=item )
    else:
        return redirect('/')

@site_bp.route('/order',methods = ['GET','POST'])
def order():
        if auth():          
            user = User.query.filter_by(username=request.cookies.get('username')).first()
            user_id = user.id
            cart = Cart.query.filter_by(user_id = user_id).first()
            cart_id= cart.id 
            total_price = 0
            for item in cart.items:
                total_price+=(item.dish.price)*(item.amount) 
            if request.method == 'POST':
                new_delivery = Delivery(
                    is_delivered = 'False',
                    user_id =user_id ,
                    adress = request.form['adress'],
                    comment = request.form['comment'],
                    created = dt.now(),
                    total_price = total_price, 
                    cart_id = cart_id 
                )
                if new_delivery.adress and new_delivery.comment!= '':                   
                    db.session.add(new_delivery) 
                    db.session.commit()

                else:
                     return 'field cant be empty'
                return redirect('/order_details')
            return render_template('site/order.html',)  
        else:
            return redirect('/')

@site_bp.route('/order_details',methods=['GET','POST'])
def order_details():
    if auth():
            user = User.query.filter_by(username=request.cookies.get('username')).first() 
            user_id = user.id
            cart = Cart.query.filter_by(user_id = user_id).first()
            cart_id = cart.id
            delivery = Delivery.query.filter_by(cart_id = cart_id).first() 
            if request.method == "GET" :
                    db.session.delete(cart)
                    db.session.commit() 
                    new_cart = Cart( user_id = user_id )
                    db.session.add(new_cart)
                    db.session.commit()  
            return render_template('site/order_details.html',cart=cart,delivery=delivery) 
    else:
        return redirect('/')

@site_bp.route('/order_history')
def order_history():    
        user = User.query.filter_by(username=request.cookies.get('username')).first() 
        delivery = Delivery.query.all() 
        return render_template('site/order_history.html',user=user , delivery=delivery) 

@site_bp.route('/edit_account_details', methods=['GET','POST'])
def edit_account_details():
    if auth():
        form = Sign_up_Form()
        user = User.query.filter_by(username=request.cookies.get('username')).first()
        if request.method == 'POST' and form.validate_on_submit():
                    user.username=form.username.data
                    user.password=form.password.data
                    user.first_name = form.first_name.data
                    user.last_name= form.last_name.data
                    user.is_staff = request.form['is_staff']
                    user.email = form.email.data
                    if user.first_name.isalpha() and user.last_name.isalpha():
                        db.session.commit()
                        return redirect(url_for('categories')) 
                    else:
                     return 'name or last name cant contain numbers'                      
        return render_template('site/edit_details.html',form = form ) 
    else:
        return redirect('/') 
