import functools
#import actions
from flask_login import current_user
from flask_socketio import disconnect, emit

from scannerDatabase import *
from scannerActions import actions
from scannerEvents import FolderEventSub, FileEventSub

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

def SocketHandler(sio):
    global FolderEventSub
    global FileEventSub

 
    def sendFolders(event,folders):
      #  print('Emitting Folders',event)
        sio.emit('SENDING_FOLDERS',folders)

    FolderEventSub+=sendFolders

    def sendFiles(event,files):
        sio.emit('SENDING_FILES',files)
    
    FileEventSub+=sendFiles

    @sio.event
    def event(message,payload):

    #    print('Event',message)
        sio.emit(message,payload)


    @sio.on('connect')
    @authenticated_only
    def connect():
        if current_user.is_authenticated:
            sio.emit('connect')
         
            sio.emit('SENDING_FOLDERS',scannerDB.folders.getFolders())
            sio.emit('SENDING_FILES',scannerDB.files.getFiles())
           

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
       