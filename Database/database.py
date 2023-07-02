from flask import Blueprint, render_template, redirect, url_for
import sqlite3
import json
from os.path import join, dirname, realpath 
from Home.home import home_bp

database_bp = Blueprint("database_bp", __name__, template_folder="templates")

def returnValuesOfDatabase(table: str):
    """Return the values from the specified table"""

    database_json = json.load(open("Globals/details/database.json"))

    conn = sqlite3.connect(database_json["filename"])
    c = conn.cursor()

    try:
        # attempt to get the infomation from the specified table
        c.execute(f"SELECT * FROM {table}")
        
    except sqlite3.OperationalError:
        # if the table does not exist

        # output that it does not exits
        print("Table does not exist")
        
        # close the database
        conn.close()

        # amd return an oempty array
        return [()]
    
    # get the result from the database
    results = c.fetchall()

    # close the database
    conn.close()

    # return the results
    return results

def getHeadings(table: str):
    database_json = json.load(open("Globals/details/database.json"))

    conn = sqlite3.connect(database_json["filename"])
    c = conn.cursor()

    try:
        # attempt to get the infomation from the specified table
        c.execute(f"PRAGMA table_info({table})")
        
    except sqlite3.OperationalError:
        # if the table does not exist
        print("Table does not exist")
        conn.close()
        return []
    
    values = c.fetchall()

    headings = []

    for value in values:
        headings.append(value[1])

    conn.close()
    print(headings)
    return headings

@database_bp.route("/")
def index():
    path = join(dirname(realpath(__file__)), "files/tables.txt") # should return fullpath to main.py + /Scripts/files
    with open(path, "r") as f:
        lines = f.readlines()
    tables = {}
    for line in lines:
        name, url = line.split(":")
        tables[name] = url.strip()

    print(tables)
    return render_template("database_home.html", tables=tables)

@database_bp.route("/list/<table>")
def listDatabase(table):
    return render_template("outputTable.html", data=returnValuesOfDatabase(table), heading=getHeadings(table))

@database_bp.route("/setup")
def setup():
    """Returns true if the username and password are in the database"""
    database_json = json.load(open("Globals/details/database.json"))

    conn = sqlite3.connect(database_json["filename"])
    c = conn.cursor()

    # create table if it does not exist
    c.execute(f"CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY, username TEXT, password TEXT, salt TEXT)")
    # and commit the (potential) changes to the database
    conn.commit()

    return redirect(url_for("home_bp.index"))