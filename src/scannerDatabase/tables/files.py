

from peewee import BigIntegerField, FloatField, IntegerField, TextField
from ..tables import BaseModle

class FilesTable(BaseModle):
    root = TextField() #ForeignKeyField(Folders,backref='folder')#
    path = TextField()
    name = TextField()
    lastAction = TextField()
    st_ino = BigIntegerField(unique=True)
    st_atime = BigIntegerField()
    st_atime_ns = BigIntegerField()
    st_birthtime=BigIntegerField()
  #  st_blksize= BigIntegerField()
    st_blocks= BigIntegerField(null=True)
    st_ctime= BigIntegerField()
    st_ctime_ns= BigIntegerField()
    st_mode= BigIntegerField()
    st_mtime= FloatField()
    st_mtime_ns= BigIntegerField()
    st_nlink=BigIntegerField()
    st_rdev=BigIntegerField(null=True)
    st_size=BigIntegerField()
    st_dev=BigIntegerField()
    st_flags= BigIntegerField(null=True)
    st_gen=BigIntegerField(null=True)
    st_gid=IntegerField()
    st_uid= BigIntegerField()



class Files():
    def __init__(self,table:FilesTable):
        self.table= table
    def addFiles(self,files: list[FilesTable]):
        try:
            self.table.insert_many(files).on_conflict('replace').execute()
           
        except Exception as e:
            print('Could not add File',e)
    def getFiles(self):
        try:
            return [file for file in self.table.select().dicts()]
        except Exception as e:
            print('Get File Error',e)
    def getFilesFromFolder(self,root:str)->list[int]:
        f =[]
        try:
            for file in self.table.select(FilesTable.st_ino).where(FilesTable.root == str(root)).dicts():
                f.append(file['st_ino'])
        
        except Exception as e:
            print('Get Files From Folder Error',e)
        return f
    def getFileByID(self,st_ino:int)->FilesTable | None:
        try:
            return self.table.get(FilesTable.st_ino==st_ino)
        except:
            print('No File Found by st_ino',st_ino)
            return None
    def getFileByName_Path(self,path,name):
        try:
            return self.table.get(FilesTable.name==name and FilesTable.root == path)
        except:
            pass
    def removeFiles(self,file_st_ino:list[int]):
        if not file_st_ino:
            return
        for st_ino in file_st_ino:
            try:
                self.table.delete().where(FilesTable.st_ino==st_ino).execute()
            except:
                print('Could not delete file', st_ino)
