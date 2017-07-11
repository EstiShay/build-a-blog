from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:ginger@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)  #Creates a database object
app.secret_key = 'clksjdtdkj45978kdjl'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    #column configured to be an integer which represents the primary key; gives each of our task objects a unique ID
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    #Provide a constructor:
    def __init__(self, name, owner):
        self.name = name
        self.completed = False
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True) #SQL will add something to the record when it's created to ensure no one can create multiple accounts with the same email
    password = db.Column(db.String(120))
    tasks = db.relationship('Task', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    #Want this to run for every request
    #Check for existance of user's email in session dictionary
    allowed_routes = ['login', 'register']

    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect ('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password: #if no user exists, then this user var will return none, which will short circuit the conditional, but if it does exist then next goes on to check the pw
            session['email'] = email
            flash("Logged in")
            print(session)
            return redirect('/')
        else:
            flash('User password incorrect or user does not exist', 'error')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        #TODO - validate the user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email #session is a dictionary
            return redirect('/')
        else:
            #TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():

    owner = User.query.filter_by(email=session['email']).first()
    #Should only be one because emails are unique but have to ask for first one; Chris didn't say why

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name, owner)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False, owner=owner).all()
    completed_tasks = Task.query.filter_by(completed=True, owner=owner).all()
    return render_template('todos.html',title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks)


@app.route("/delete-task", methods=["POST"])
def delete_task():
    #Handler function

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()
    #This shields the app.run call so that it's only run if I run main.py; can import other parts of the code into other applications/files etc.  Will allow me to import the Task class or any of the other objects into another Python session or Python file