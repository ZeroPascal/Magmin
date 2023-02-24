import datetime
from Tools.Scans.scanFolder import scanFolder
from db import Folder, addFolder, getFiles, getFolder, removeFolder, updateFolderLastScan
from events import Events, FileEvents, FolderEvents



def addDirectory(name:str,root:str,recursive:bool): #, callback:Callable[[None],list[Folder]]):
   # addFolder(root,name,recursive,callback)
    FolderEvents(Events.ADD_FOLDER,addFolder(root,name,recursive))

def removeDirectory(name:str):
    FolderEvents(Events.REMOVE_FOLDER,removeFolder(name))

def scanDirectory(name:str):
    scanFolder(getFolder(name))

def updateDirectoryScanTime(root:str,time:int):
    #updateFolderLastScan(root,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    FileEvents(Events.UPDATED_FOLDER,getFiles())
    FolderEvents(Events.UPDATED_FOLDER,updateFolderLastScan(root,time))
    