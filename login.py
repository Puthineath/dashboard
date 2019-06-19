from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/admin')
db = client.admin

db_user = db.users


@app.route('/')
def index():
    # if 'username' in session:
    #     return 'You are logged in as ' + session['username']
    if request.method == 'POST':
      session['username'] = request.form['username']
      return render_template('index.html')
    return render_template('login.html')
 

    
@app.route('/login', methods=['POST','GET'])
def login():
    
    login_user = db.users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        
        existing_user = db.users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            db.users.insert_one({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

if __name__ == '__main__':
    
    app.run(debug=True)