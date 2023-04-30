from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField,SubmitField,RadioField,SelectField,TextAreaField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,Email,NumberRange
class Sign_up_Form(FlaskForm):
    username = StringField("Username",validators=[DataRequired("Please enter a username."),
        Length(5,15,"Username length must be 5 to 15")
    ])
    password = PasswordField("Password",validators=[DataRequired("Please enter a password.")])
    first_name = StringField("first_name",validators=[DataRequired("Please enter a first name.")])
    last_name = StringField("last_name",validators=[DataRequired("Please enter a last name."),DataRequired("Please enter a password.")])
    is_staff = SelectField("is_staff",choices=[('True','True'),('False','False')])   
    email = StringField("Email",validators=[Email("Please enter a valid email address.")])
    submit = SubmitField("Sign Up") 

class edit_category_form(FlaskForm):
    category_name = StringField("category_name",validators=[DataRequired("Please enter a category name.")])
    category_image = StringField("category_image",validators=[DataRequired("Please enter  image name.")])

class edit_dish_form(FlaskForm):
    name = StringField("name",validators=[DataRequired("Please enter a dish name.")])
    price = IntegerField("price",validators=[DataRequired("Please enter a dish price.")])
    description =StringField("description",validators=[DataRequired("Please enter a dish description.")])
    image = StringField("image",validators=[DataRequired("Please enter dish image .")])


class add_category_form(FlaskForm):
    category_name = StringField("category_name",validators=[DataRequired("Please enter a category name .")])
    category_image = StringField("category_image",validators=[DataRequired("Please enter  image .")])

class add_dish_form(FlaskForm):
    name = StringField("name",validators=[DataRequired("Please enter a dish name.")])
    description =StringField("description",validators=[DataRequired("Please enter a dish description.")])
    image = StringField("image",validators=[DataRequired("Please enter dish image .")])
    price = IntegerField('price', validators=[DataRequired('please enter price '),NumberRange(min=0),
    ])
    
# @app.route('/sign_up',methods=['GET','POST']) 
# def sign_up():
#         form = Sign_up_Form()
#         if auth():
#          return redirect('/categories')
#         elif request.method == 'POST' and form.validate_on_submit():               
#                 new_user = User(form.username.data,
#                                 form.password.data,
#                                 form.first_name.data,
#                                 form.last_name.data,
#                                 form.is_staff.data,
#                                 form.email.data
#                 )
#                 db.session.add(new_user)
#                 db.session.commit()
#                 new_cart = Cart( user_id = new_user.id)
#                 db.session.add(new_cart)
#                 db.session.commit()
#                 return redirect('/log_in') 
#         return render_template('sign_upp.html',form=form)


# @app.route('/sign_up',methods=['GET','POST'])
# def sign_up():
#         if auth():
        
#          return redirect('/categories')
#         elif request.method == 'POST':
#                 try:
                     
#                     first_name=request.form['first_name']
#                     last_name=request.form['last_name']
#                     if first_name.isalpha() and last_name.isalpha():                     
#                         new_user = User(
#                         username=request.form['username'],
#                         password=request.form['password'],
#                         first_name=request.form['first_name'],
#                         last_name=request.form['last_name'],
#                         is_staff=request.form['is_staff'],
#                         email=request.form['email'] 
#                         )
#                         db.session.add(new_user)
#                         db.session.commit()
#                         new_cart = Cart( user_id = new_user.id)
#                         db.session.add(new_cart)
#                         db.session.commit()
#                         return redirect('/log_in') 
#                     else :
#                         return 'names cant include numbers'
#                 except:
#                      return 'try again , remember to not leave empty fields '
#         return render_template('sign_up.html')
