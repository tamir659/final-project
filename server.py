from flask import Flask ,render_template,request,redirect,make_response,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt 
from forms import Sign_up_Form , edit_category_form , edit_dish_form , add_category_form,add_dish_form

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'ju43hgri2347rs'

db = SQLAlchemy()
db.init_app(app) 

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    first_name = db.Column(db.String(200),nullable=False)
    last_name = db.Column(db.String(200),nullable=False)
    is_staff = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    deliveries = db.relationship('Delivery',backref ='user') 

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False,unique=True)
    image = db.Column(db.String(200),nullable=False)
    dishes = db.relationship('Dish',backref = 'category')

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

class Cart(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) 
    deliveries = db.relationship('Delivery',backref='cart',uselist=False)
    items = db.relationship('Items',backref = 'cart') 

class Items(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    dish_id = db.Column(db.Integer,db.ForeignKey('dish.id'))
    cart_id = db.Column(db.Integer,db.ForeignKey('cart.id'))
    amount = db.Column(db.Integer,nullable=False)

class Delivery(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    is_delivered = db.Column(db.String(200),nullable=False)
    adress = db.Column(db.String(200),nullable=False)
    comment = db.Column(db.String(200),nullable=False)
    created = db.Column(db.DateTime)
    total_price = db.Column(db.Integer,nullable=False) 
    cart_id = db.Column(db.Integer,db.ForeignKey('cart.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
     
with app.app_context():
    db.create_all()
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


@app.route('/')
def main():
     if auth():
        return redirect('/categories')
     else:
        return render_template('main.html') 


@app.route('/sign_up',methods=['GET','POST']) 
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
        return render_template('sign_up.html',form=form)

@app.route('/log_in',methods = ['GET','POST']) 
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
    return render_template('log_in.html')

@app.route('/staff_log_in',methods = ['GET','POST'])
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
     return render_template('staff_log_in.html') 

@app.route('/categories')
def categories():
    user = User.query.filter_by(username=request.cookies.get('username')).first()
    if auth():
        category = Category.query.all()
        return render_template('categories.html',category=category,user=user)
    else:
        return redirect('/') 

@app.route('/show_category_dishes/<int:id>')
def show_category_dishes(id):
    if auth():
        category=Category.query.get(id) 
        return render_template('show_category_dishes.html',category=category) 
    else:
        return redirect('/')

@app.route('/show_dish/<int:id>',methods=['GET','POST'])
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
        return render_template('show_dish.html',dish=dish) 
    else:
        return redirect('/') 

@app.route('/sign_out')
def sign_out():
    resp = make_response(redirect('/'))
    resp.delete_cookie('username')
    return resp 

@app.route('/cart')
def cart():
    if auth():
        dish = Dish.query.all() 
        user = User.query.filter_by(username=request.cookies.get('username')).first() 
        user_id = user.id
        cart = Cart.query.filter_by(user_id = user_id).first()
        total_price = 0
        for item in cart.items:
                total_price+=(item.dish.price)*(item.amount) 
        return render_template('cart.html',cart=cart,dish=dish,total_price=total_price) 
    else:
        return redirect('/')
    
@app.route('/order',methods = ['GET','POST'])
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
            return render_template('order.html',)  
        else:
            return redirect('/')

@app.route('/order_details',methods=['GET','POST'])
def order_details():
    if auth():
                user = User.query.filter_by(username=request.cookies.get('username')).first() 
                user_id = user.id
                cart = Cart.query.filter_by(user_id = user_id).first()
                cart_id = cart.id
                delivery = Delivery.query.filter_by(cart_id = cart_id).first() 
                return render_template('order_details.html',cart=cart,delivery=delivery) 
    else:
        return redirect('/')

@app.route('/order_history')
def order_history():    
        user = User.query.filter_by(username=request.cookies.get('username')).first() 
        delivery = Delivery.query.all() 
        return render_template('order_history.html',user=user , delivery=delivery) 

@app.route('/orders_manage')
def orders_manage():
     if auth():
        if is_staff_auth():
            delivery = Delivery.query.all()
            return render_template('orders_manage.html',delivery=delivery)
        else:
             return redirect('/categories')  
     else:
          return redirect('/')   
@app.route('/remove_item/<int:id>',methods = ['GET','POST'])
def remove_item(id):
    if auth():
        item=Items.query.get(id) 
        if request.method == 'POST':
                    db.session.delete(item)
                    db.session.commit()
                    return redirect('/cart') 
        return render_template('remove_item.html',item=item )
    else:
        return redirect('/')
    
@app.route('/edit_account_details', methods=['GET','POST'])
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
                     
        return render_template('edit_details.html',form = form ) 
    else:
        return redirect('/')
    
@app.route('/main_staff')
def main_staff():
    if auth():
            if is_staff_auth():
                user = User.query.filter_by(username=request.cookies.get('username')).first()
                return render_template('main_staff.html',user = user )
            else:
                 return redirect('/categories') 
    else:
        return redirect('/')    

@app.route('/staff_categories')
def staff_categories():
    if auth():
            if is_staff_auth():
                user = User.query.filter_by(username=request.cookies.get('username')).first()
                category = Category.query.all()
                return render_template('staff_categories.html',category=category,user=user) 
            else:
                 return redirect('/categories')     
    else:
        return redirect('/')

@app.route('/add_category', methods=['GET','POST'])
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
                return render_template('add_category.html',form=form) 
            else:
                 return redirect('/categories')
    else:
        return redirect('/')
    
@app.route('/staff_show_category_dishes/<int:id>')
def staff_show_category_dishes(id):
    if auth():
            if is_staff_auth():
                category=Category.query.get(id) 
                return render_template('staff_show_category_dishes.html',category=category)
            else:
                 return redirect('/categories')
    else:
        return redirect('/')

@app.route('/add_dish/<int:id>', methods=['GET','POST'])
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
                return render_template('add_dish.html',category=category,form=form)
            else:
                 return redirect('/categories') 
    else:
        return redirect('/')
    
@app.route('/delite_dish/<int:id>',methods=['GET','POST'])
def delite_dish(id):
    if auth():
            if is_staff_auth():
                dish=Dish.query.get(id)
                if request.method == 'POST':
                    db.session.delete(dish)
                    db.session.commit()
                    return redirect('/staff_categories')            
                return render_template('delite_dish.html',dish=dish)
            else:
                 return redirect('/categories') 
    else:
        return redirect('/')
    
@app.route('/edit_dish/<int:id>',methods=['GET','POST'])
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
                return render_template('edit_dish.html',dish=dish,form=form)
            else:
                 return redirect('/categories')
     else:
        return redirect('/')
     
@app.route('/delite_category/<int:id>',methods=['GET','POST'])
def delite_category(id):
    if auth():
            if is_staff_auth():
                category=Category.query.get(id)
                if request.method == 'POST':
                    db.session.delete(category)
                    db.session.commit()
                    return redirect('/staff_categories')            
                return render_template('delite_category.html',category=category)
            else:
                 return redirect('/categories') 
    else:
        return redirect('/')
@app.route('/edit_category/<int:id>',methods=['GET','POST'])
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
                return render_template('edit_category.html', category=category,form=form)
            else:
                 return redirect('/categories') 
    else:
        return redirect('/')

@app.route('/change_to_delivered/<int:id>',methods=['GET','POST'])
def change_to_delivered(id):
    delivery = Delivery.query.get(id)
    if request.method == 'POST':
          delivery.is_delivered = 'True'
          db.session.commit()
          return redirect('/orders_manage')
    return render_template('change_to_delivered.html',delivery=delivery) 
          
app.run(debug=True)   

