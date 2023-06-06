from flask import Flask 
from db import db 
from routes.site import site_bp
from routes.staff import staff_bp
from config import DBUSER,DBHOST,DBPASS
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/postgres'
app.config['SECRET_KEY'] = 'ju43hgri2347rs'

db.init_app(app) 


with app.app_context():
    db.create_all()

app.register_blueprint(staff_bp)
app.register_blueprint(site_bp) 
          
app.run(debug=True,host="0.0.0.0")     

