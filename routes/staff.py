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
from forms import edit_category_form , edit_dish_form , add_category_form,add_dish_form 

staff_bp = Blueprint('staff',__name__)  
   
@staff_bp.route('/staff_log_in',methods = ['GET','POST'])
def staff_log_in():
     if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user != None:
        
         if user.is_staff == 'True':
            if user.password == request.form['password']:
                resp = make_response(redirect('/main_staff')) 
                resp.set_cookie('username',user.username) 
                return resp 
            else:
                return'password or username incorrect' 
         else:
             return 'you are not a staff member'
     return render_template('/staff/staff_log_in.html') 

@staff_bp.route('/orders_manage')
def orders_manage():
     if auth():
        if is_staff_auth():
            delivery = Delivery.query.all()
            return render_template('/staff/orders_manage.html',delivery=delivery)
        else:
             return redirect('/categories')  
     else:
          return redirect('/')   
    
@staff_bp.route('/main_staff')
def main_staff():
    if auth():
            if is_staff_auth():
                user = User.query.filter_by(username=request.cookies.get('username')).first()
                return render_template('/staff/main_staff.html',user = user )
            else:
                 return redirect('/categories') 
    else:
        return redirect('/')    

@staff_bp.route('/staff_categories')
def staff_categories():
    if auth():
            if is_staff_auth():
                user = User.query.filter_by(username=request.cookies.get('username')).first()
                category = Category.query.all()
                return render_template('/staff/staff_categories.html',category=category,user=user) 
            else:
                 return redirect('/categories')     
    else:
        return redirect('/')

@staff_bp.route('/add_category', methods=['GET','POST'])
def add_category():
    if auth():
            if is_staff_auth():
                form = add_category_form()
                if request.method == 'POST' and form.validate_on_submit():
                    new_category = Category(
                        name = form.category_name.data,
                        image= form.category_image.data
                        )               
                    if new_category.name.isalpha():                     
                        db.session.add(new_category)
                        db.session.commit()
                        return redirect('/staff_categories')
                    else:
                        'category name cant be empty or contain numbers'     
                return render_template('/staff/add_category.html',form=form) 
            else:
                 return redirect('/categories')
    else:
        return redirect('/')
    
@staff_bp.route('/staff_show_category_dishes/<int:id>')
def staff_show_category_dishes(id):
    if auth():
            if is_staff_auth():
                category=Category.query.get(id) 
                return render_template('/staff/staff_show_category_dishes.html',category=category)
            else:
                 return redirect('/categories')
    else:
        return redirect('/')

@staff_bp.route('/add_dish/<int:id>', methods=['GET','POST'])
def add_dish(id):
    if auth():
            if is_staff_auth():
                form = add_dish_form()
                category=Category.query.get(id) 
                if request.method == 'POST' and form.validate_on_submit():
                    
                    new_dish = Dish(
                        name = form.name.data,
                        price = form.price.data,
                        description = form.description.data,
                        image= form.image.data,
                        is_gluten_free = request.form['is_gluten_free'],
                        is_vegeterian = request.form['is_vegeterian_free'],
                        category_id = id 
                        )
                    db.session.add(new_dish)
                    db.session.commit()
                    return redirect('/staff_categories') 
                return render_template('/staff/add_dish.html',category=category,form=form)
            else:
                 return redirect('/categories') 
    else:
        return redirect('/')
    
@staff_bp.route('/delite_dish/<int:id>',methods=['GET','POST'])
def delite_dish(id):
    if auth():
            if is_staff_auth():
                dish=Dish.query.get(id)
                if request.method == 'POST':
                    db.session.delete(dish)
                    db.session.commit()
                    return redirect('/staff_categories')            
                return render_template('/staff/delite_dish.html',dish=dish)
            else:
                 return redirect('/categories') 
    else:
        return redirect('/')
    
@staff_bp.route('/edit_dish/<int:id>',methods=['GET','POST'])
def edit_dish(id):
     if auth():
            if is_staff_auth():
                form = edit_dish_form()
                dish=Dish.query.get(id)
                if request.method == 'POST' and form.validate_on_submit():
                        dish.name=form.name.data 
                        dish.price=form.price.data
                        dish.description = form.description.data
                        dish.image= form.image.data
                        dish.is_gluten_free = request.form['is_gluten_free']
                        dish.is_vegeterian = request.form['is_vegeterian']
                        db.session.commit()
                        return redirect(url_for('staff_categories'))
                return render_template('/staff/edit_dish.html',dish=dish,form=form)
            else:
                 return redirect('/categories')
     else:
        return redirect('/')
     
@staff_bp.route('/delite_category/<int:id>',methods=['GET','POST'])
def delite_category(id):
    if auth():
            if is_staff_auth():
                category=Category.query.get(id)
                if request.method == 'POST':
                    db.session.delete(category)
                    db.session.commit()
                    return redirect('/staff_categories')            
                return render_template('/staff/delite_category.html',category=category)
            else:
                 return redirect('/categories') 
    else:
        return redirect('/')
@staff_bp.route('/edit_category/<int:id>',methods=['GET','POST'])
def edit_category(id): 
    if auth():
            if is_staff_auth():
                form= edit_category_form()  
                category= Category.query.get(id) 
                if request.method == 'POST' and form.validate_on_submit():                   
                    category.name=form.category_name.data               
                    category.image= form.category_image.data
                    category_name = form.category_name.data 
                    if category_name.isalpha():
                        db.session.commit()
                        return redirect(url_for('staff_categories'))
                    else:
                        return 'category name cant contain numbers'                        
                return render_template('/staff/edit_category.html', category=category,form=form)
            else:
                 return redirect('/categories') 
    else:
        return redirect('/')

@staff_bp.route('/change_to_delivered/<int:id>',methods=['GET','POST'])
def change_to_delivered(id):
    delivery = Delivery.query.get(id)
    if request.method == 'POST':
          delivery.is_delivered = 'True'
          db.session.commit()
          return redirect('/orders_manage')
    return render_template('/staff/change_to_delivered.html',delivery=delivery) 
          
