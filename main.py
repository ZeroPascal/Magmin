import os, os.path
import string
import json
import cherrypy
from cherrypy.lib import auth_digest
from cherrypy import tools

from db import *
from index import getIndex


class Admin(object):
    @cherrypy.expose
    def index(self):
        authHeader =cherrypy.request.headers['Authorization']
        user = authHeader[authHeader.index('"')+1:authHeader.index(',')-1]
        server = getUser('server')
        info = {
            'user': user,
            'serverKey': server.password
        }
        return open("./site/index.html") #getIndex(info)#

    @cherrypy.expose 
    @cherrypy.tools.json_out()
    def settings(self):
        authHeader =cherrypy.request.headers['Authorization']
        user = authHeader[authHeader.index('"')+1:authHeader.index(',')-1]
        server = getUser('server')
        info = {
            'user': user,
            'serverKey': server.password
        }
        print(info)
        return (info)

class SetAPIService(object):
    exposed = True
    def POST(self,apiURL,apiKEY):
        print('Data',apiURL,apiKEY)
        return {apiURL:'got it'}

def setup_database():
    start_database()

if __name__ == "__main__":

    cherrypy.engine.subscribe("start", setup_database)
    USERS = getAdmins()
    #print('Admins',USERS)
    conf = {
        "/": {
            "tools.sessions.on": True,
            "tools.staticdir.root": os.path.abspath(os.getcwd()),
            "tools.auth_digest.on": True,
            "tools.auth_digest.realm": "localhost",
            "tools.auth_digest.get_ha1": auth_digest.get_ha1_dict_plain(USERS),
            "tools.auth_digest.key": "a565c27146791cfb",
        },
        "/SetAPI":{
             'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
             'tools.response_headers.on': True,
        },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './public'
         }
    }
    webapp = Admin()
    webapp.SetAPI = SetAPIService()
    cherrypy.quickstart(webapp,"/",conf)