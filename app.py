from datetime import datetime, date, timedelta

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///management.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    genre = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

@app.route('/', methods =['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()
        today = date.today()
        yesterday = date.today() + timedelta(days=2)
        return render_template('index.html', posts=posts, today=today, yesterday=yesterday)
    else:
        purchase = request.form.get('purchase')
        title = request.form.get('title')
        genre = request.form.get('genre')
        detail = request.form.get('detail')
        due = request.form.get('due')
        
        purchase = datetime.strptime(purchase, '%Y-%m-%d')
        due = datetime.strptime(due, '%Y-%m-%d')
        new_post = Post(purchase=purchase, title=title, genre=genre, detail=detail, due=due)
        
        db.session.add(new_post)
        db.session.commit()
        
        return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.purchase = datetime.strptime(request.form.get('purchase'), '%Y-%m-%d')
        post.title = request.form.get('title')
        post.genre = request.form.get('genre')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')
        
        db.session.commit()
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)
    
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()