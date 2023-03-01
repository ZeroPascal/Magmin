import logging
import os
from pathlib import Path
import sys
from flask import Flask, redirect,request, send_from_directory, url_for
from flask_socketio import SocketIO
from scannerDatabase import ScannerDatabase,scannerDB
from .socketHandler import SocketHandler
from flask_login import LoginManager, login_required, login_user, logout_user



def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    p = os.path.join(os.path.abspath("."), relative_path)
    print(p)
    return os.path.join(os.path.abspath("."), relative_path)

def path():
    #root= os.path.abspath(os.path.dirname(__file__))
    root = Path(__file__).parent.parent.parent
    src = os.path.join(root,'static')
    return src


app = Flask(__name__,static_url_path='')


login_manager = LoginManager()
login_manager.init_app(app)
sio = SocketIO(app,logger=False,engineio_logger=False)
login_manager.login_view = 'login'
#scannerDB = None
def start_server( server_secret:'str',host='0.0.0.0', port='5001'):
    global app
    global sio
 #   global scannerDB
    app.secret_key=server_secret
    #scannerDB=database
    sio.run(app,host=host, port=port) 

SocketHandler(sio)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@login_manager.user_loader
def load_user(username):
    global scannerDB
    try:
        a = scannerDB.users.checkAdmin(username)
        return a
    except:
        return None
def getUserRights(header:request):
    print(header)
@app.route('/login', methods=['GET', 'POST'])
def login():
    global scannerDB
    if request.method == 'POST':
        user = scannerDB.users.checkAdmin([request.form['username']])
        if not user:
            return """No User Found"""
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
    

