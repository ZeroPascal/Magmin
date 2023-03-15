

from typing import TypedDict
from peewee import BigIntegerField, BooleanField, TextField
from ..tables import BaseModle



class Folder(TypedDict):
        name: str
        root: str
        recursive: bool
        lastScan: int

    #def __init__(self,name:str,root:str,recursive:bool,lastScan:int):
     #   self.name=name
      #  self.root=root
       # self.recursive=recursive
        #self.lastScan=lastScan


class FoldersTable(BaseModle):
    root = TextField(unique=True)
    name = TextField(unique=True)
    lastScan = BigIntegerField()
    recursive = BooleanField()

class Folders():
    def __init__(self,table:FoldersTable):
        self.table= table
        
    def addFolder(self,root:str,name:str,recursive:bool): #,callback:Callable[[None],list[Folder]]):
        if root !='' and name !='':
            try:
                self.table.create(root=root,name=name,recursive=recursive, lastScan='0')
            except Exception as e:
                print('Failed To Make Folder',name)
                print(e)
                pass
        return(self.getFolders())

    def removeFolder(self,name:str):
        try:
            deadFolder = self.table.get(FoldersTable.name==name)
            self.table.delete().where(FoldersTable.root ==deadFolder.root).execute()
          #  self.table.delete().where(self.table.name==name).execute()
        except Exception as e:
            print('Could not delete folder:',name)
            print(e)

        return(deadFolder)
    def updateFolderLastScan(self,folderName:str,time):
        try:
            folder =self.table.get(FoldersTable.name==folderName)
            folder.lastScan= time
            folder.save()
        except Exception as e:
            print('Folder LastScan Update Failed',e)
        return(self.getFolders())
    def getFolders(self):
        folders: list[Folder] = []
        try:
            for f in self.table.select(FoldersTable):
                folder = Folder(name=f.name,root=f.root,recursive=f.recursive,lastScan=f.lastScan)
                folders.append(folder)
        except Exception as e:
            print('Failed To get Folders',e)
            pass
        return folders
    def getFolder(self,name:str):
        try:
            f= self.table.get(FoldersTable.name==name)
            return Folder(name=f.name,root=f.root,recursive=f.recursive,lastScan=f.lastScan)
        except:
            return Folder()