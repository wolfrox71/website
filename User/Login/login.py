from flask import Blueprint, session, redirect, url_for, render_template, request
import Globals.global_functions as global_functions
import json
import sqlite3

login_bp = Blueprint("login_bp", __name__, template_folder="templates")

def detailsCorrect(username: str, password: str) -> bool:
    """Returns true if the username and password are in the database"""
    database_json = json.load(open("Globals/details/database.json"))

    conn = sqlite3.connect(database_json["filename"])
    c = conn.cursor()

    # get all the data where the username and password match the username and password provided by the users login screen
    c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    conn.commit()
    results = c.fetchall()

    # close the database 
    conn.close()

    # if any result exist then the user exists so return true
    return len(results) > 0

def usernameInUse(username:str) -> bool:
    """Returns if a username is in use"""
    database_json = json.load(open("Globals/details/database.json"))

    conn = sqlite3.connect(database_json["filename"])
    c = conn.cursor()

    c.execute(f"SELECT * FROM users WHERE username='{username}'")
    conn.commit()
    results = c.fetchall()

    conn.close()

    return len(results) > 0

def getSalt(username: str) -> str:
    """Returns the salt for a given username"""
    database_json = json.load(open("Globals/details/database.json"))

    conn = sqlite3.connect(database_json["filename"])
    c = conn.cursor()

    c.execute(f"SELECT salt FROM users WHERE username='{username}'")
    conn.commit()
    salt = c.fetchone()[0]

    conn.close()

    print(f"SALT: {salt}")

    return salt
    
def insertUser(username: str, password: str, salt: str):
    """Insert the username and hashed password, and salt to hash the password into the database"""
    database_json = json.load(open("Globals/details/database.json"))

    # if the user already exists
    if usernameInUse(username):
        # return so that it does not create the user
        return

    # the userExists check also creates the table if it does not already exist 

    # connect to the database specified in the infomation file
    conn = sqlite3.connect(database_json["filename"])
    c = conn.cursor()

    c.execute(f"SELECT MAX(userID) FROM users")

    count = c.fetchone()[0]
    if count is None:
        print("No users exist")
        count = 0
    else:
        print(f"COUNT: {count}")
    count += 1

    # insert the username and password into the table
    c.execute(f"INSERT INTO users VALUES ('{count}', '{username}', '{password}', '{salt}')")
    conn.commit()

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
        if not usernameInUse(request.form["username"]):
            # send the user back to the login screen
            return f"""<p>User does not exists</p><br><a href={url_for('user_bp.login_bp.login')}>Login Screen</a>"""
        
        salt = getSalt(request.form["username"])

        hashed_password = global_functions.hashString(request.form["password"] ,salt)

        if not detailsCorrect(request.form["username"], hashed_password):
            return f"""<p>Details Incorrect</p><br><a href={url_for('user_bp.login_bp.login')}>Login Screen</a>"""

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
        
        if (usernameInUse(request.form["username"])):
            return f"""<p>Username already in use</p><br><a href={url_for('user_bp.login_bp.createUser')}>Create User</a>"""

        # generate a salt for this user
        salt = global_functions.generateSalt()

        # hash the password using this users salt
        hashed_password = global_functions.hashString(request.form["password1"], salt)
        
        # insert the username, hashed password, and salt into the database
        insertUser(request.form["username"], hashed_password, salt)
        return request.form