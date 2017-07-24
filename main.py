from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
# to use the SQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
# allows you to query 
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)
# secret key is needed for session management
app.secret_key = "jalsejiofjakfgjka"


# database class
class Entry(db.Model):

    # database table columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(500))
    datecreated = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        # ties specific entries with Entry class to owner (or user)
        self.owner = owner 
        # date created for ordering entries
        self.datecreated = datetime.utcnow()

    #validation 
    def validation(self):
        if self.title and self.body and self.datecreated:
            return True
        else:
            return False


# user class
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    # ties specific entries with Entry class to owner (or user)
    entries = db.relationship("Entry", backref="owner")

    def __init__(self, username, password):
        self.username = username 
        self.password = password


# requires login
@app.before_request
def require_login():
    # whitelist for allowed routes
    # allows someone to view login, signup, and blog entries without signing in
    # user view FUNCTION to whitelist, not URL path
    allowed_routes = ["login", "signup", "blog", "index"]

    # if path isn't in whitelist and user not logged in
    # redirects to login page 
    if request.endpoint not in allowed_routes and "username" not in session:
        redirect("/login")


# redirects to blog page for convenience
@app.route("/")
def index():
    return redirect("/blog")


# main blog page
# displays all blog entries
@app.route("/blog", methods=["POST", "GET"])
def blog():

    # displays entries in chrono order
    all_entries = Entry.query.all()
    
    # from Al's code: shows all entries in reverse chronological order
    #all_entries = Entry.query.order_by(Entry.datecreated.desc()).all()

    # show specific entry
    entry_id = request.args.get("id")
    if (entry_id):
        entry = Entry.query.get(entry_id)
        return render_template("one_entry.html", title="Blog Entry", entry=entry)

        
    #renders all entries
    return render_template("mainpage.html", title="All Blog Entries", all_entries=all_entries)


@app.route("/new_entry", methods=["POST", "GET"])
def new_entry():

    if request.method == "POST":
        new_title = request.form["title"]
        new_body = request.form["body"]
        new_entry = Entry(new_title, new_body)


        # validation

        # if valid input
        if new_entry.validation():
            # add to database
            db.session.add(new_entry)
            db.session.commit()
            # redirect to new entry
            return redirect("/blog?id=" + str(new_entry.id))
        else:
            # error message
            flash("A title and a body are required to submit an entry")
            # render template again, including any user input
            return render_template("new_entry.html", title="New Blog Entry", new_title=new_title, new_body=new_body)

    else: 
        # renders empty form
        return render_template("new_entry.html", title="New Blog Entry")


# TODO user signup page
@app.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        # TODO add in validation from user signup assignment

        # checks if user already exists in database
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            # creates new user
            new_user = User(username, password)
            # adds new user to database 
            db.session.add(new_user)
            db.session.commit()
            # adds username to session
            session["username"] = username
            return redirect("/blog")
        else: 
            flash("Username already exists.", "error")

    return render_template("signup.html")


# login page
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # returns user with a specific username, if it exists
        user = User.query.filter_by(username=username).first()
        # compares user and password
        if user and user.password == password:
            # adds username to session
            session["username"] = username 
            flash("Logged in.")
            return redirect("/blog")
        else: 
            flash("User password incorrect, or user does not exist.", "error") 

    return render_template("login.html")


# logout
@app.route("/logout")
def logout():
    # removes username from session
    del session["username"]
    return redirect("/blog")


# TODO 
#@app.route("/")
#def index():
    #pass 
    #return render_template("index.html")



if __name__ == '__main__':
    app.run()


# for displaying by user
# owner = User.query.filter_by(username=session["username"]).first()