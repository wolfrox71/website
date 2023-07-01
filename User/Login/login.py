from flask import Blueprint, session, redirect, url_for, render_template, request
import Globals.global_functions as global_functions
import json
import sqlite3

login_bp = Blueprint("login_bp", __name__, template_folder="templates")

def userExists(username: str, password: str) -> bool:
    database_json = json.load(open("Globals/details/database.json"))

    conn = sqlite3.connect(database_json["filename"])
    c = conn.cursor()

    # create table if it does not exist    
    c.execute(f"CREATE TABLE IF NOT EXISTS {database_json['table']} (userID, username, password)")
    # and commit the (potential) changes to the database
    conn.commit()


    # get all the data where the username and password match the username and password provided by the users login screen
    c.execute(f"SELECT * FROM {database_json['table']} WHERE username={username} AND password={password}")
    conn.commit()
    results = c.fetchall()

    # if any result exist then the user exists so return true
    return len(results) > 0

@login_bp.route("/")
def index():
    isLoggedIn: bool = global_functions.validSessionID()
    if isLoggedIn:
        status = ""
    else:
        status = "not "
    return render_template("login_home.html", status=status)

@login_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login_page.html")
    
    if request.method == "POST":
        # if the user does not exist
        if userExists(request.form["username"], request.form["password"]) == False:
            # send the user back to the login screen
            return redirect(url_for("user_bp.login_bp.login"))
        
        # at this point the user does exist in the database
        # so add the values from the from to the session
        session["username"] = request.form["username"]

        # generate the sessionID for the session with this new infomation
        session["sessionID"] = global_functions.generateSessionID()
        
        # return the user to the index page of the website now that the user is logged in 
        return redirect(url_for("home_bp.index"))

@login_bp.route("/logout")
def logout():
    del session["sessionID"]
    return redirect(url_for("home_bp.index"))

@login_bp.route("/createUser", methods=["POST", "GET"])
def createUser():
    if request.method == "GET":
        return render_template("create_user.html")
    
    if request.method == "POST":
        # if the passwords to not match
        if (request.form["password1"] != request.form["password2"]):
            # reload the page to get other values
            return redirect(url_for("user_bp.login_bp.createUser"))
        return request.form