from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///joinhands.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show Events Registered"""
    events = db.execute(
        "SELECT events.name, events.date FROM events INNER JOIN user_events ON events.id = user_events.event_id WHERE user_events.id = ? ORDER BY events.date;", session["user_id"])
    # list of dictionary with events posted and username joined
    posts = db.execute("SELECT events.name AS event_name, users.username AS joined_username FROM events JOIN user_events ON events.id = user_events.event_id JOIN users ON users.id = user_events.id WHERE events.host = ?;", session["user_id"])
    return render_template("index.html", events = events, posts = posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("username can't be empty")
        if not password:
            return apology("password can't be empty")
        if password != request.form.get("confirmation"):
            return apology("confirmation doesn't match")

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, generate_password_hash(password))
        except ValueError:
            return apology("username already exists")

         # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Remember which user has logged in (auto log in)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "POST":
        name = request.form.get("event")
        date = request.form.get("date")
        num = request.form.get("people")
        if not name or not date:
            return apology("Make sure you fill all field")
        if not num or not num.isdigit() or int(num) <= 0:
            return apology("amount must be a positive number")
        
        try:
            db.execute("INSERT INTO events (host, name, date, people_num) VALUES (?, ?, ?, ?);", session["user_id"], name, date, num)
        except ValueError:
            return apology("name already used")
        return redirect("/")
    else:
        return render_template("post.html")
    
@app.route("/signup", methods=["GET", "POST"])
@login_required
def signup():
    """Sell shares of stock"""
    if request.method == "POST":
        name = request.form.get("event")
        # get the event id
        event = db.execute("SELECT id FROM events WHERE name = ?;", name)[0]["id"]
        if not event:
            return apology("must select event")
        rows = db.execute("SELECT * FROM user_events WHERE id = ? AND event_id = ?;", session["user_id"], event)
        if len(rows) > 0:
            return apology("You can only register once for the same event.")
        db.execute("INSERT INTO user_events (id, event_id) VALUES (?, ?)",
                   session["user_id"], event)

        return redirect("/")
    else:
        #dictionary of all the event names
        all = db.execute(
            "SELECT id, name, date FROM events ORDER BY id DESC;")
        #produce list of dictionary of only those not full
        open = []
        for row in all:
            current_num = db.execute(
                "SELECT COUNT (*) as count FROM user_events WHERE event_id = ?;", row["id"])[0]["count"]
            max_num = int(db.execute(
                "SELECT people_num FROM events WHERE id = ?;", row["id"])[0]["people_num"])
            if current_num < max_num:
                open.append({"name": row["name"], "date": row["date"]})
        return render_template("signup.html", open=open)
