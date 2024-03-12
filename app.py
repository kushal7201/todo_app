from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" # Use a relative path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class MyTodo(db.Model):
    __tablename__ = 'todo'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    desc = db.Column(db.String(350), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"({self.sno}) {self.title}"

with app.app_context():
    db.create_all()

@app.route('/', methods = ['GET','POST'])
def Todo():
    todos = MyTodo.query.all()
    if request.method == "POST":
        print("ToDo List added successfully")
        title = request.form['title']
        desc = request.form['desc'] # name = "title" must be there in the html element
        todo = MyTodo(title=title, desc =desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('Todo'))
    else:
        return render_template('index.html', todos=todos)

@app.route('/update/<int:sno>', methods = ['GET','POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc'] # name = "title" must be there in the html element
        todo = MyTodo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        print("ToDo updated successfully")
        return redirect('/')

    todo = MyTodo.query.filter_by(sno=sno).first()    
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todos = MyTodo.query.filter_by(sno=sno).first()
    db.session.delete(todos)
    db.session.commit()
    return redirect(url_for('Todo'))

@app.route('/home')
def home():
    return 'We are home'

