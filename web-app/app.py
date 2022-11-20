from flask import Flask, render_template, request,session, redirect, url_for
from bson.json_util import dumps
from mongodb import Database
Database.initialize
app=Flask(__name__)

@app.route('/')
def home():
    if 'username' in session:
        return 'Welcome'+session['username']
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    user = Database.find_single("user", {"username": request.form["username"]})
    if (user and user['password'] == request.form["password"]):
        session['username'] = request.form["password"]
        return redirect(url_for('home'))
    return 'Invalid username or password!'

@app.route('/register', methods=['GET','POST'])
def register():
    if(request.method=='POST'):
        username = request.form['username']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password = request.form['password']
        if (username and firstName and lastName and password):
            user = Database.find_single("user", {"username": request.form["username"]})
            if (user is None):
                Database.insert_one("user", {'username': username, 'firstName': firstName,
                                    'lastName': lastName, 'password': password})
                return redirect(url_for('home'))
            else:
                return 'Username is already taken!'
    return render_template('register.html')

if __name__=='__main__':
    app.run(debug=True)
