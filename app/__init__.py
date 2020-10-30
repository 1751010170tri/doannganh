from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = "\x8fM\xef\xd2\x9f\x0cl\x13\xa7\t\xd7\xc3\x156\x07\xb4"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/qlhs?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
admin = Admin(app=app,name="QLHS",template_mode="bootstrap3")
login = LoginManager(app=app)