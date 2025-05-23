import logging
import os
from pathlib import Path
import sys
from flask import Flask, redirect,request, send_from_directory, url_for, abort
from flask_socketio import SocketIO
from scannerDatabase import ScannerDatabase,scannerDB
from definitions import ROOT_DIR, THUMBNAIL_DIR
from .socketHandler import SocketHandler
from flask_login import LoginManager, login_required, login_user, logout_user



def path():
    #root= os.path.abspath(os.path.dirname(__file__))
    print('Root',ROOT_DIR)
    root = Path(ROOT_DIR)
    src = os.path.join(root,'static')   
    return src


app = Flask(__name__,static_folder=path(),static_url_path='')
print('Static Location',app.static_folder)
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
    sio.run(app,host=host, port=port, allow_unsafe_werkzeug=True ) 

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

@app.route('/tumbnail/<path:filename>')
def get_image(filename):

    # Only allow files with safe extensions
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    file_ext = os.path.splitext(filename)[1].lower()
   
    if file_ext not in allowed_extensions:
       # print('invalid extension')
        abort(400, description="Invalid file extension")

    # Prevent path traversal
    if '..' in filename or filename.startswith('/'):
        #print('format error')
        abort(400, description="Invalid filename")
    try:
        return send_from_directory('thumbnails',filename)
    except FileNotFoundError:  
        print('File Not found') 
        abort(404, description="File not found")

if __name__ == '__main__': 
    print('Started')
    sio.run(app,host='0.0.0.0', port='5001')  # Start the server Host 0.0.0.0 to listen on machine ip
    