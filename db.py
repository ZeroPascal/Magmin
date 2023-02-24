from typing import Callable, TypedDict
from peewee import *
from playhouse.shortcuts import model_to_dict
from enum import Enum
import uuid

class UserRights(Enum):
    ADMIN = '1'
    READ_WRIGHT = '2'
    READ_ONLY = '3'
    WRIGHT_ONLY ='4'
    
db = SqliteDatabase('./database.db')

class Folder(TypedDict):
    name:str
    root:str
    recursive:bool
    lastScan: int

class BaseModle(Model):
    class Meta:
        database = db
class Users(BaseModle):
    user = TextField(unique=True)
    password = TextField(null=False)
    rights = TextField(null=False)

class Server(BaseModle):
    apiURL = TextField(unique=True,null=False)
    apiKEY = TextField()

class Folders(BaseModle):
    root = TextField(unique=True)
    name = TextField(unique=True)
    lastScan = BigIntegerField()
    recursive = BooleanField()

class Files(BaseModle):
    root = TextField() #ForeignKeyField(Folders,backref='folder')#
    path = TextField()
    name = TextField()
    lastAction = TextField()
    st_ino = BigIntegerField(unique=True)
    st_atime = BigIntegerField()
    st_atime_ns = BigIntegerField()
    st_birthtime=BigIntegerField()
    st_blksize= BigIntegerField()
    st_blocks= BigIntegerField()
    st_ctime= BigIntegerField()
    st_ctime_ns= BigIntegerField()
    st_mode= BigIntegerField()
    st_mtime= FloatField()
    st_mtime_ns= BigIntegerField()
    st_nlink=BigIntegerField()
    st_rdev=BigIntegerField()
    st_size=BigIntegerField()
    st_dev=BigIntegerField()
    st_flags= BigIntegerField()
    st_gen=BigIntegerField()
    st_gid=IntegerField()
    st_uid= BigIntegerField()

def hashPassword(pwd:str):
    #Currently disabled until I can figure out ha1_dict in cherrypy conf
    #return hashlib.md5(pwd.encode()).hexdigest()
    return pwd
def start_database():
 
    db.create_tables([Users,Server,Folders,Files])

    try:
        Users.create(user='admin',password=hashPassword('admin'),rights=UserRights.ADMIN.name)
        Users.create(user='server',password=hashPassword(uuid.uuid4()), rights=UserRights.READ_WRIGHT.name)
    except Exception as e:
        print('Could Not Create Default User',e)

def addFiles(files: list[Files]):
        try:
            Files.insert_many(files).on_conflict('replace').execute()
           
        except Exception as e:
            print('Could not add File',e)
def getFiles():
    try:
        return [file for file in Files.select().dicts()]
    except Exception as e:
        print('Get File Error',e)
def getFilesFromFolder(root:str)->list[int]:
    try:
        f =[]
        for file in Files.select(Files.st_ino).where(Files.root == root).dicts():
            f.append(file['st_ino'])
        return f
    except Exception as e:
       print('Get Files From Folder Error',e)
def getFileByID(st_ino:int)->Files:
    try:
        return Files.get(Files.st_ino==st_ino)
    except:
        pass
def getFileByName_Path(path,name):
    try:
        return Files.get(Files.name==name and Files.root == path)
    except:
        pass
def addFolder(root:str,name:str,recursive:bool): #,callback:Callable[[None],list[Folder]]):
    if root !='' and name !='':
        try:
            Folders.create(root=root,name=name,recursive=recursive, lastScan='0')
        except:
            return
    print('AddedFolder')
    getFolders()
    #callback(getFolders())
    return(getFolders())
def removeFiles(file_st_ino:list[int]):
    if not file_st_ino:
        return
    for st_ino in file_st_ino:
        try:
            Files.delete().where(Files.st_ino==st_ino).execute()
        except:
            print('Could not delete file', st_ino)
def removeFolder(name:str):
    try:
        deadFolder = Folders.get(Folders.name==name)
        Files.delete().where(Files.root ==deadFolder.root).execute()
        Folders.delete().where(Folders.name==name).execute()
        
    except:
        print('Could not delete folder:',name)

    return(getFolders())
def updateFolderLastScan(path,time):
    try:
        folder =Folders.get(Folders.root == path)
        folder.lastScan= time
        folder.save()
    except Exception as e:
        print('Folder LastScan Update Failed',e)
    return(getFolders())
def getFolders():
    folders: list[Folder] = []
    for f in Folders:
        folder = Folder()
        folder['name'] = f.name
        folder['root'] = f.root
        folder['recursive'] =f.recursive
        folder['lastScan'] = f.lastScan
        folders.append(folder)
    return folders
def getFolder(name:str):
    try:
        return Folders.get(Folders.name==name)
    except:
        return False
def setAPI(apiKey:str, apiURL:str = None):
    try:
        Server.insert(id=1,apiKEY=apiKey,apiURL=apiURL).on_conflict('replace').execute()
    except Exception as e:
        print('Could not update API Info',e)
def getUser(username:str='admin'):
    try:
        user :Users =Users.get(Users.user == username)
        return user
    except:  
        print('Error Fetching User',username)
   
def getAPI():
    return Server.get(id=1)
def getAdmins():
    admins:Users = Users.select(Users).where(Users.rights == UserRights.ADMIN.name)
    adminDic = {}
    for a in admins:
        adminDic[a.user] = a.password
 
    return adminDic

def getServerKey():
    return Users.get(Users.user=='server').password