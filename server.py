from flask import Flask 
from db import db 
from routes.site import site_bp
from routes.staff import staff_bp
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'ju43hgri2347rs'

db.init_app(app) 


with app.app_context():
    db.create_all()

app.register_blueprint(staff_bp)
app.register_blueprint(site_bp) 
          
app.run(debug=True)   

