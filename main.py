from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:doanglick@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)  #Creates a database object
app.secret_key = 'jumj@st1ck'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    #column configured to be an integer which represents the primary key; gives each of our task objects a unique ID
    title = db.Column(db.String(220))
    entry = db.Column(db.String(2000))
    
    #Provide a constructor:
    def __init__(self, title, entry):
        self.title = title
        self.entry = entry


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        title_name = request.form['title']
        blog_entry = request.form['entry']
        new_blog = Blog(title_name, blog_entry)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    # completed_tasks = Task.query.filter_by(completed=True, owner=owner).all()
    return render_template('blog.html',title="My Launch Code Blog", blogs=blogs)



if __name__ == '__main__':
    app.run()
    #This shields the app.run call so that it's only run if I run main.py; can import other parts of the code into other applications/files etc.  Will allow me to import the Task class or any of the other objects into another Python session or Python file