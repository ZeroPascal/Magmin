import datetime
from scannerTools import scanFolder
from scannerDatabase import *
from scannerEvents import *




def addDirectory(name:str,root:str,recursive:bool): #, callback:Callable[[None],list[Folder]]):
    # addFolder(root,name,recursive,callback)
    FolderEventSub(FolderEvents.ADD_FOLDER,scannerDB.folders.addFolder(root,name,recursive))

def removeDirectory(name:str):
    FolderEventSub(FolderEvents.REMOVE_FOLDER,scannerDB.removeFolder(name))

def scanDirectory(name:str):
    scanFolder(scannerDB.folders.getFolder(name))

def updateDirectoryScanTime(folderName:str,time:int):
        #updateFolderLastScan(root,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    FileEventSub(FolderEvents.UPDATED_FOLDER,scannerDB.files.getFiles())
    FolderEventSub(FolderEvents.UPDATED_FOLDER,scannerDB.folders.updateFolderLastScan(folderName,time))
    