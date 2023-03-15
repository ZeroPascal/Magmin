from enum import Enum
import uuid
from typing import TypedDict

from peewee import *
from .tables import *




#class Server(BaseModle):
#    apiURL = TextField(unique=True,null=False)
#    apiKEY = TextField()



class ScannerDatabase():
    def __init__(self):
        self.baseModle = BaseModle()
        self.users = Users(UsersTable(self.baseModle))
        self.folders= Folders(FoldersTable(self.baseModle))
        self.files= Files(FilesTable(self.baseModle))
        self.db = db
        self.db.create_tables([UsersTable(self.baseModle),FoldersTable(self.baseModle),FilesTable(self.baseModle)])
        self.users.makeDefaultUsers()
    
    def removeFolder(self,name:str):
        try:
            deadFolder = self.folders.removeFolder(name)
            self.files.removeFilesByFolder(deadFolder.root)
        except Exception as e:
            print('Could not delete folder:',name)
            print(e)

        return(self.folders.getFolders())

    
scannerDB = ScannerDatabase()


