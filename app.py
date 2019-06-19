from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
import bcrypt

application = app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/admin')
db = client.admin

db_customer_order = db.customer_order_test
db_payment = db.payment_test
db_pages = db.pages
db_customer = db.customer
db_user = db.users


@app.route('/')
def index():
    if session.get('email') is not None:
        if session['email']:
            return render_template('index.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    


@app.route('/login', methods=['POST'])
def login():
    
    login_user = db.users.find_one({'name' : request.form['email']})

    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['email'] = request.form['email']
            return redirect(url_for('index'))

    return 'Invalid email/password combination'

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
    app.secret_key = 'mysecret'
    app.run(debug=True)



