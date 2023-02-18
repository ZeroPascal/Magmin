from peewee import *
from enum import Enum
import uuid

class UserRights(Enum):
    ADMIN = '1'
    READ_WRIGHT = '2'
    READ_ONLY = '3'
    WRIGHT_ONLY ='4'
    
db = SqliteDatabase('./database.db')

class BaseModle(Model):
    class Meta:
        database = db
class Users(BaseModle):
    user = TextField(unique=True)
    password = TextField(null=False)
    rights = TextField(null=False)

def hashPassword(pwd:str):
    #Currently disabled until I can figure out ha1_dict in cherrypy conf
    #return hashlib.md5(pwd.encode()).hexdigest()
    return pwd
def start_database():
 
    db.create_tables([Users])
    try:
        Users.create(user='admin',password=hashPassword('admin'),rights=UserRights.ADMIN.name)
        Users.create(user='server',password=hashPassword(uuid.uuid4()), rights=UserRights.READ_WRIGHT.name)
    except Exception as e:
        print('Could Not Create Default User',e)



def getUser(username:str='admin'):
    try:
        user :Users =Users.get(Users.user == username)
        return user
    except: 
        print('Error Fetching User',username)
   

def getAdmins():
    admins:Users = Users.select(Users).where(Users.rights == UserRights.ADMIN.name)
    adminDic = {}
    for a in admins:
        adminDic[a.user] = a.password
 
    return adminDic

