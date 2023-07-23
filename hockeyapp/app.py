import requests
import os
from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
import datetime
from flask_session import Session
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash
import pyodbc

server = "cesprojectserver.database.windows.net"
database = 'CES Database'
username = 'zkeschner'
password = '@Mitchellk11'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
@app.route("/")
def home():
    if request.method == 'GET':
        return render_template('home.html')

@app.route("/register", methods= ["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        if not name or not password or not confirm:
            return "oops"
        if confirm != password:
            return "Ops"
        passhash = generate_password_hash(password)
        db = cnxn.cursor()
        db.execute("insert into users(username, hash) values (?, ?)", name, passhash)
        cnxn.commit()

    else:
        return render_template("register.html")
    return redirect("/")
@app.route("/login", methods= ["GET", "POST"])
def login():
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return "OOPS" # apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "oops" #apology("must provide password", 403)
        db = cnxn.cursor()
        db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        unames = []
        for rows in db:
            unames += rows
        #print(unames)
        #print(unames[2])
        # Ensure username exists and password is correct
        print(len(unames))
        if len(unames) != 3 or not check_password_hash(unames[2], request.form.get("password")):
            return "OOOPS" #apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = unames[0]
        print(session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/stick", methods= ["POST", "GET"])
@login_required
def stick():
    if request.method == "GET":
        db = cnxn.cursor()
        db.execute("select * from sticks where id = ?", session["user_id"])
        table = []
        for row in db:
            temp = []
            temp += row
            #print(temp)
            table.append(temp)
        #print(table)
        return render_template("stick.html", table = table)
    else:
        check = request.form["check"]
        db = cnxn.cursor()
        db.execute("insert into reserve select * from sticks where Primaryid = ?", check)
        db.execute("delete from sticks where PrimaryID = ?", check)
        cnxn.commit()
        return redirect("/stick")
@app.route("/info", methods= ["POST", "GET"])
@login_required
def info():
    return render_template("info.html")

@app.route("/list", methods=["POST", "GET"])   
@login_required
def list():
    if request.method == "POST":

        user_id = session["user_id"]
        brand = request.form.get("brand")
        flex = request.form.get("flex")
        size = request.form.get("size")
        curve = request.form.get("curve")
        hand = request.form.get("hand")
        model = request.form.get("model")
        address = request.form.get("address")
    
        if (hand.upper() not in ["RIGHT", "LEFT"]):
            return "Invalid Hand"
        db = cnxn.cursor()
        db.execute("insert into sticks(id, brand, sticksize, flex, curve, hand, model, address) values (?, ?, ?, ?, ?, ?, ?,?)", user_id, brand, size, flex, curve, hand, model, address)
        cnxn.commit()
        return render_template("home.html")
    else:
        return render_template("list.html")
@app.route("/reserved", methods=["POST","GET"])
@login_required
def reserved():
    if request.method == "GET":
        db = cnxn.cursor()
        user_id = session["user_id"]
        db.execute("select * from reserve where id = ?", user_id)
        table = []
        for row in db:
            temp = []
            temp += row
            #print(temp)
            table.append(temp)
            print(table)
        return render_template("reserve.html", table=table)
    else:
        return
if __name__ == "__main__":
    app.run()