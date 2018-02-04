from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:letsbuild@localhost:8889/buildablog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/')
def index():
    blogs = Blog.query.all() 
    #needs to list all blogs from database
    return render_template('index.html', blogs=blogs)


@app.route('/displaypost')
def show():
    displayid = request.args.get("blogid")
    blogs = Blog.query.get(displayid)
    return render_template('displaypost.html',blog = blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost(): 
    if request.method == "GET":
        return render_template('newpost.html')

    title = request.form['title']
    body = request.form['body']

    if not (title or body):
        return render_template('newpost.html', title = 'Please add a title', body = 'Please share your thoughts') 

    blog_instance = Blog(title, body)
    db.session.add(blog_instance)
    db.session.commit()

    return redirect("/")
    




if __name__ == '__main__':
    app.run()