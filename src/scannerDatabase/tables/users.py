from enum import Enum
from typing import TypedDict
import uuid
from flask_login import UserMixin
from peewee import TextField
from ..tables import BaseModle


class UserRights(Enum):
    ADMIN = '1'
    READ_WRIGHT = '2'
    READ_ONLY = '3'
    WRIGHT_ONLY ='4'
    
class User(TypedDict):
    username: str
    password: str
    rights: UserRights

class UserLogin(UserMixin):
    def __init__(self, username:str, password:str):
        self.username = username
        self.password= password
    def get_id(self):
        return (self.username)


class UsersTable(BaseModle):
    username = TextField(unique=True)
    password = TextField(null=False)
    rights = TextField(null=False)


def hashPassword(pwd:str):
    #Currently disabled until I can figure out ha1_dict in cherrypy conf
    #return hashlib.md5(pwd.encode()).hexdigest()
    return pwd

class Users():
    def __init__(self, table:UsersTable):
        self.users =[]
        self.table =table
    def makeDefaultUsers(self):
        try:
            UsersTable.create(username='admin',password=hashPassword('admin'),rights=UserRights.ADMIN.name)
            UsersTable.create(username='server',password=hashPassword(uuid.uuid4()), rights=UserRights.READ_WRIGHT.name)
        except Exception as e:
            print('Could Not Create Default User',e)
    def getAdmins(self):
        admins:dict[UserLogin] ={}
        for user  in self.table.select(UsersTable).where(UsersTable.rights==UserRights.ADMIN).dict():
            admin = UserLogin(user)
            admins[admin.username] = admin
        return admins
    def checkAdmin(self,username):
        try:
            #user = self.table.select().where(UsersTable.user==username and UsersTable.rights==UserRights.ADMIN).dict()
            #user = self.table.get(self.table.user =='admin') #.dict()
            user = self.table.select(UsersTable).where(UsersTable.rights==UserRights.ADMIN and UsersTable.username == username).get()
          #  print(user.username)
            if user:
           #     print(user['user'])
                return UserLogin(username=user.username, password=user.password)
        except Exception as e:
            print('User Check Error',e)
            return None
    def getRights(self,username)->UserRights | None:
        try:
            user = self.table.get(UsersTable.username ==username)
            return username.rights
        except:
            return None
    def getServerKey(self):
        return self.table.get(self.table.user=='server').password
    
    def getUser(self,username:str='admin'):
        try:
            user:User =self.table.get(UsersTable.user == username).dict()
            return user
        except:  
            print('Error Fetching User',username)
            return None
            