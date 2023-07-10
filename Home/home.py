from flask import Blueprint, render_template
from os.path import join, dirname, realpath

home_bp = Blueprint("home_bp", __name__, template_folder="../templates/Home/")

def getPaths(filename="paths.txt"):
    filepath = join(dirname(realpath(__file__)), filename) # join the path to this file + the path to the text file with the values in
    with open(filepath, "r") as f:
        lines = f.readlines()
    paths = {}
    
    for line in lines:
        path, name = line.split(":")
        paths[path] = name.strip()
    return paths


@home_bp.route("/")
def index():
    print(getPaths())
    return render_template("Home_index.html", paths=getPaths())