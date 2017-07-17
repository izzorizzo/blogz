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
class Task(db.Model):

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, name, owner):
        self.name = name
        self.completed = False 
        self.owner = owner 

# User class
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    # populate this tasks list with things from the class 
    # task such that the owner property is specific to user
    tasks = db.relationship("Task", backref="owner")

    def __init__(self, email, password):
        self.email = email
        self.password = password


# checks if user has logged in before
@app.before_request
def require_login():
    # lets user see login and register pages 
    # to login/register if previous session doesn't exist
    allowed_routes = ["login", "register"]
    if request.endpoint not in allowed_routes and "email" not in session:
        return redirect("/login")


# login page
@app.route("/login", methods=["POST", "GET"])
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
            flash("User password incorrect, or user does not exist", "error")

    return render_template("login.html")


# register page
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        verify = request.form["verify"]

        # TODO - validate user's data

        # check if existing user
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            # remembers if user has logged in before
            session["email"] = email
            return redirect("/")
        else: 
            # TODO - user better response messaging
            return "<h1>Duplicate user!</h1>"       

    return render_template("register.html")


@app.route("/logout")
def logout():
    del session["email"]
    return redirect("/")


# main form
@app.route('/', methods=['POST', 'GET'])
def index():

    # assigns task to owner
    owner = User.query.filter_by(email=session["email"]).first()

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name, owner)
        db.session.add(new_task)
        db.session.commit() 

    # filters out completed tasks
    tasks = Task.query.filter_by(completed=False, owner=owner).all() 
    # completed tasks
    completed_tasks = Task.query.filter_by(completed=True, owner=owner).all() 
    return render_template('todos.html',title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)


# delete tasks 
@app.route('/delete-task', methods=["POST"])
def delete_task():

    # gets task id and marks it as completed using a Boolean
    task_id = int(request.form["task-id"])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    #returns user to index page
    return redirect('/')

if __name__ == '__main__':
    app.run()