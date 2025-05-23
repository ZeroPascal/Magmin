

from peewee import BigIntegerField, FloatField, IntegerField, TextField
from ..tables import BaseModle

class FilesTable(BaseModle):
    root = TextField() #ForeignKeyField(Folders,backref='folder')#
    path = TextField()
    name = TextField()
    suffix= TextField()
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
    VFormat= TextField(null=True)
    VCodecID= TextField(null=True)
    VBitRate= TextField(null=True)
    VWidth=IntegerField(null=True)
    VHeight=IntegerField(null=True)
    VFrameRateMode= TextField(null=True)
    VFrameRate= TextField(null=True)
    VDuration=IntegerField(null=True)
    VFrameCount=IntegerField(null=True)
    VEncoder=TextField(null=True)
    VCreationTime= TextField(null=True)
    AFormat= TextField(null=True)
    AFormatSettings= TextField(null=True)
    ACodecID= TextField(null=True)
    ADuration= TextField(null=True)
    AChannels= TextField(null=True)
    AChannelsLayout= TextField(null=True)
    ASamplingRate= TextField(null=True)
    ABitDepth= TextField(null=True)

class Files():
    def __init__(self,table:FilesTable):
        self.table= table
    def addFiles(self,files: list[FilesTable]):
        try:
            for file in files:
             #   print(file)
                self.table.insert(file).on_conflict('replace').execute()
          #  self.table.insert_many(files).on_conflict('replace').execute()
           
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
            return list(self.table.select().where(FilesTable.st_ino==st_ino).dicts())[0]
        except:
          #  print('No File Found by st_ino',st_ino)
            return None
    def getFileByName_Path(self,path,name):
        try:
            print('Getting File',path,name)
            return self.table.get(FilesTable.name==name,FilesTable.root == path)
          #  return self.table.select().where(FilesTable.name==name and FilesTable.root ==path)
        except:
            pass
    def removeFilesByFolder(self,root):
        try:
            self.table.delete().where(FilesTable.root==root).execute()
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
