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

    # TODO change 

    # database table columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(500))
    datecreated = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body 

# redirects to blog page for convenience
@app.route("/")
def index():
    return redirect("/blog")


# main blog page
# displays all blog entries
@app.route("/blog", methods=["POST", "GET"])
def blog():
    #TODO if request.method == "POST":
    

        

    return render_template("mainpage.html", title="All Entries")


@app.route("/new_entry", method=["POST", "GET"])
def new_entry():
    if request.method == "POST":
        new_title = request.form["title"]
        new_entry = request.form["body"]

        # validation
        if new_title == "" or new_entry == "":
            # error message
            flash("A title and a body are required to submit an entry", "error")
            # render template again, including anything user input
            return render_template("new_entry.html", title="New Blog Entry", new_title=new_title, new_entry=new_entry)
        # if no errors, add entry to database
        else:
            db.session.add(new_entry)
            db.session.commit()

        # TODO redirect to specific entry
        # return redirect("blog?id=" + str())

    if request.method == "GET":
        return render_template("new_entry.html", title="New Blog Entry")




if __name__ == '__main__':
    app.run()