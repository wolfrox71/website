from flask import Blueprint, render_template
from os import walk
from os.path import join, dirname, realpath

scripts_bp = Blueprint("script_bp", __name__, template_folder="templates")

def return_files(path="files/"):
    full_path = join(dirname(realpath(__file__)),path) # should return fullpath to main.py + /Scripts/files
    filenames = next(walk(full_path), (None, None, []))[2]  # [] if no file
    return filenames

def file_contents(filename, path="files/"):
    dir_path = join(dirname(realpath(__file__)),path) # should return fullpath to main.py + /Scripts/files
    file_path = join(dir_path, filename)
    with open(file_path, "r") as f:
        return f.read()

@scripts_bp.route("/")
def index():
    return render_template("home.html", scripts=return_files())

@scripts_bp.route("<id>")
def script(id):
    return file_contents(id)