import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = "74fe13370e062efda7e52bc7aa7336c2" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/werda/Desktop/TodoApp/todo.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from todo import routes