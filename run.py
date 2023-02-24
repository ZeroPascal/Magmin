import base64
import json
import logging
import os
import sys
from typing import TypedDict
from flask import Flask, jsonify, redirect,request, url_for
from flask_socketio import SocketIO
from db import getAdmins, getServerKey, start_database
from socketHandler import SocketHandler
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

start_database()
app = Flask(__name__, static_url_path='') #resource_path('static') )
app.secret_key = getServerKey()
login_manager = LoginManager()
login_manager.init_app(app)
sio = SocketIO(app,logger=False,engineio_logger=False)

login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self):
        self.username =''
        self.password=''
    
    def get_id(self):
        return self.username

class Users(TypedDict):
    username:str
    user: User

users: Users ={}
USERS = getAdmins()
for user in USERS:
    u = User()
    u.username = user
    u.password =USERS[user]
    users[user] = u

@login_manager.user_loader
def load_user(username):
    try:
        return users[username]
    except:
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = users[request.form['username']]
        if user.password != request.form['password'] :
            error = 'Invalid Credentials. Please try again.'
        else:
            u = load_user(request.form['username'])
            login_user(user=u,remember=True)
            return redirect(url_for('home'))
    return """ <form action="" method="post">
        <input type="text" placeholder="Username" name="username">
         <input type="password" placeholder="Password" name="password" >
        <input class="btn btn-default" type="submit" value="Login">
      </form>"""

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

SocketHandler(sio)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/') 
@login_required
def home():
    return app.send_static_file('index.html')  # Return index.html from the static folder

@app.route('/API/addDirectory/<directory>', methods=['POST']) 
@login_required
def addDirectory(directory:str):
    print(directory)
    return "Okay"

if __name__ == '__main__': 
    print('Started')
    sio.run(app,host='0.0.0.0', port='5001')  # Start the server Host 0.0.0.0 to listen on machine ip
    


