from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
# to use the SQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
# allows you to query 
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "jalsejiofjakfgjka"


# database class
class Entry(db.Model):

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, name, owner):
        self.name = name
        self.completed = False 
        self.owner = owner 


# redirects to blog page for convenience
@app.route("/")
def index():
    return redirect("/blog")


# main blog page
@app.route("/blog", methods=["POST", "GET"])
def login ():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            # remembers if user has logged in before
            session["email"] = email 
            # flash message after login
            flash("Logged In")
            print(session)
            return redirect("/")
        else:
           # flash("User password incorrect, or user does not exist", "error")

    return render_template("login.html")



if __name__ == '__main__':
    app.run()