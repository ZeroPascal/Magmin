import functools
import actions
from flask_login import current_user
from flask_socketio import disconnect, emit
from db import Folder, getFiles, getFolders
from events import FolderEvents, FileEvents

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

def SocketHandler(sio):
    global FolderEvents
    global FileEvents
    def sendFolders(event,folders):
        sio.emit('SENDING_FOLDERS',folders)

    FolderEvents+=sendFolders

    def sendFiles(event,files):
        sio.emit('SENDING_FILES',files)
    
    FileEvents+=sendFiles

    @sio.event
    def event(message,payload):

        print('Event',message)
        sio.emit(message,payload)


    @sio.on('connect')
    @authenticated_only
    def connect():
        if current_user.is_authenticated:
            sio.emit('connect')
            sio.emit('SENDING_FOLDERS',getFolders())
            sio.emit('SENDING_FILES',getFiles())

        else:
            return 

    @sio.on('ADD_DIRECTORY')
    def addDirectory(folder:Folder):
        actions.addDirectory(name=folder['name'],root=folder['root'],recursive=folder['recursive']) #,callback=sendFolders)

    @sio.on('REMOVE_DIRECTORY')
    def removeDirectory(folderName:str):
        actions.removeDirectory(name=folderName)

    @sio.on('SCAN_DIRECTORY')
    def scanDirectory(folderName:str):
        actions.scanDirectory(name=folderName)