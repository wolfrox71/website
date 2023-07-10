from flask import Blueprint, render_template

random_bp = Blueprint("random_bp", __name__, template_folder="../templates/Random/")

@random_bp.route("/")
def index():
    return render_template("Random_home.html", paths={})