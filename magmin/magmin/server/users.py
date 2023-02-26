
from typing import TypedDict
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self):
        self.username =''
        self.password=''
    
    def get_id(self):
        return self.username

class Users(TypedDict):
    username:str
    user: User

