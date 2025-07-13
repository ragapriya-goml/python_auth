from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

# ❌ Insecure function usage
user_input = input("Enter command: ")
eval(user_input)

# ❌ Hardcoded credentials
password = "superSecret123"

# ❌ Unsafe system call
import os
os.system("rm -rf /")

# Example vulnerable code to test your bot
import os
import subprocess

# 🚨 SQL Injection vulnerability
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL injection risk
    return execute_query(query)

# 🚨 Command injection vulnerability  
def backup_file(filename):
    os.system(f"cp {filename} /backup/")  # Command injection risk

# 🚨 Path traversal vulnerability
def read_file(filename):
    with open(f"/data/{filename}", 'r') as f:  # Path traversal risk
        return f.read()

# 🚨 Hardcoded credentials
API_KEY = "sk-1234567890abcdef"  # Hardcoded secret
DATABASE_PASSWORD = "admin123"   # Hardcoded password

# 🚨 Unsafe eval
def calculate(expression):
    return eval(expression)  # Code injection risk

class Todo(db.Model):
  id=db.Column(db.Integer, primary_key=True)
  content=db.Column(db.String(200),nullable=False)
  date_created=db.Column(db.DateTime,default=datetime.utcnow)
  
  def __repr__(self):
    return '<Task %r>' % self.id
  
@app.route('/', methods=['POST','GET'])
def index():
  if request.method=='POST':
    task_content=request.form['content']
    new_task=Todo(content=task_content)
    
    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue adding your task'
  else:
    tasks=Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html',tasks=tasks)
  
@app.route('/delete/<int:id>')
def delete(id):
  task_to_delete=Todo.query.get_or_404(id)
  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return 'There was a problem deleting that task'
  
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
  task=Todo.query.get_or_404(id)
  
  if request.method=='POST':
    task.content=request.form['content']
    
    try:
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue updating your task'
  else:
    return render_template('update.html',task=task)


if __name__=='__main__':
  app.run(debug=True)
