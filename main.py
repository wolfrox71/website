from flask import Flask, Blueprint, url_for, render_template, redirect, session
from Home.home import home_bp
from User.user import user_bp
from Scripts.scripts import scripts_bp

app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(scripts_bp, url_prefix="/script")

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

if __name__ == "__main__":
    app.run(debug=True)