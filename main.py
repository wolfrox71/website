from flask import Flask, Blueprint, url_for, render_template, redirect, session
from Home.home import home_bp
from User.user import user_bp
from Database.database import database_bp
from Scripts.scripts import scripts_bp
from Random.random import random_bp

app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(scripts_bp, url_prefix="/script")
app.register_blueprint(database_bp, url_prefix="/database")
app.register_blueprint(random_bp, url_prefix="/random")

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

if __name__ == "__main__":
    app.run(debug=True)