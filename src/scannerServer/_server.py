import logging
import os
import sys
from flask import Flask, redirect,request, url_for
from flask_socketio import SocketIO
from scannerDatabase import ScannerDatabase
from .socketHandler import SocketHandler
from flask_login import LoginManager,  login_required, login_user, logout_user

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class FlaskWrapper(object):
    #https://dev.to/nandamtejas/implementing-flask-application-using-object-oriented-programming-oops-5cb
    def __init__(self, app, **configs):
        self.app = app
        self.configs(**configs)

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)

#app = Flask(__name__, static_url_path='')
#login_manager = LoginManager()
#sio = SocketIO(app,logger=False,engineio_logger=False)
#SocketHandler(sio)
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

class ScannerServer():

  #  global login_manager
   # global sio
    def __init__(self,scannnerDB:ScannerDatabase,secret_key:str):
        self.scannerDB = scannnerDB
        self.app =Flask(__name__, static_url_path='')
        self.app.secret_key = secret_key
        self.login_manager = LoginManager()
        self.sio = SocketIO(self.app,logger=False,engineio_logger=False)
        #SocketHandler(sio)
        self.log = logging.getLogger('werkzeug')
        self.log.setLevel(logging.ERROR)
        self.login_manager.login_view = 'login'
        self.sio.run(self.app,host='0.0.0.0', port='5001') 


    @self.login_manager.user_loader
    def load_user(self,username):
        try:
            return self.scannerDB.users.checkAdmin(username)
        except:
            return None

    @app.route('/login', methods=['GET', 'POST'])
    def login(self):
        if request.method == 'POST':
            user = self.scannerDB.users.getUser([request.form['username']])
            if user.password != request.form['password'] :
                error = 'Invalid Credentials. Please try again.'
            else:
                u = self.load_user(request.form['username'])
                login_user(user=u,remember=True)
                return redirect(url_for('home'))
        return """ <form action="" method="post">
            <input type="text" placeholder="Username" name="username">
            <input type="password" placeholder="Password" name="password" >
            <input class="btn btn-default" type="submit" value="Login">
        </form>"""

    @app.route('/logout', methods=['GET', 'POST'])
    def logout(self):
        logout_user()
        return redirect(url_for('home'))

    @app.route('/') 
    @login_required
    def home(self):
        return app.send_static_file('index.html')  # Return index.html from the static folder

    @app.route('/API/addDirectory/<directory>', methods=['POST']) 
    @login_required
    def addDirectory(self,directory:str):
        print(directory)
        return "Okay"

if __name__ == '__main__': 
    print('Started')
    sio.run(app,host='0.0.0.0', port='5001')  # Start the server Host 0.0.0.0 to listen on machine ip
    

