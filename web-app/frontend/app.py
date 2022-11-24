from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import dotenv_values

import pymongo
import calendar
import datetime
from bson.objectid import ObjectId
import sys
import os

# instantiate the app
app = Flask(__name__, template_folder='html',
            static_folder='static')


@app.route('/')
def show_home():
    return render_template('index.html')

@app.route('/logout')
def show_logout():
    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def show_main():   

    if(1==0):
        return render_template('loginFail.html')
    
    userId="2099"
    mood="sad"
    img="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/800px-Image_created_with_a_mobile_phone.png"
    return render_template('main.html',userId=userId,mood=mood,img=img)

@app.route('/register')
def show_create():

    return render_template('register.html')

@app.route('/createAccount', methods=['GET', 'POST'])
def show_createResult():   

    if(1==0):
        return render_template('creatFail.html')
    
    return render_template('createSuccess.html')

port = int(os.environ.get('PORT', 5000))
app.run(debug=True, host='0.0.0.0', port=port)
