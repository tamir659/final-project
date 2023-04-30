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
    
