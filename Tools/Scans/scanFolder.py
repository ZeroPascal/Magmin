
import datetime
import json
import os
import stat
from pathlib import Path, PosixPath
from db import Folder, addFiles, getFileByID, getFileByName_Path, getFilesFromFolder, getFolder, removeFiles
import actions

ignoreExtenstions = []#['.txt']
def checkExtenstion(ex:str):
    try:
        return ignoreExtenstions.index(ex) == 0
    except:
        return True

#https://stackoverflow.com/questions/55638905/how-to-convert-os-stat-result-to-a-json-that-is-an-object
def stat_to_json(s_obj:stat) -> dict:
    return {k: getattr(s_obj, k) for k in dir(s_obj) if k.startswith('st_')}

def processScan(path:PosixPath,files):
    known_children = getFilesFromFolder(path.as_posix())
    new_files = []
    for file in files:
   #     print(file['name'])
        try:

            known_children.remove(file['st_ino'])
            file['lastAction']=''
            f = getFileByID(file['st_ino'])
            if f:
                #print('     File Already Exists')
                if f and f.name != file['name']:
                    print('Name Change:',file['name'])
                    file['lastAction']= 'Name Change'
                    new_files.append(file)
                if f and f.st_mtime != file['st_mtime']:
                    print('Modified',file['name'], type(f.st_mtime), type(file['st_mtime']))
            else:
                print('Issuse:',file['name'])
                raise 'New File'
        except:
        #    print('     New Or Modified File')
            f= getFileByName_Path(path=path.as_posix(),name=file['name'])
            print(f)
            if f:
                print('File Changed:',file['name'])
                file['lastAction']='Modified'
            else:
                print('New File:',file['name'])
                file['lastAction']='New'
        new_files.append(file)

      #  print('File ',file['name'],file['lastAction'])
    if len(new_files)==0 and len(known_children) ==0:
        print('No Changes to:',path)
    
    addFiles(new_files)
    removeFiles(known_children)
   # print(known_children)
                     

def scanFolder(folder:Folder):
    files =[]
    path = Path(folder.root)
    if path.exists():
        for child in path.iterdir():
            if child.is_file() and checkExtenstion(child.suffix):
                j = stat_to_json(os.stat(child))
                j['name'] = child.name
                j['root'] = folder.root
                j['path'] = child.absolute()
                files.append(j)
        

        processScan(path,files)
        actions.updateDirectoryScanTime(path,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    else:
        print('No Such Path',path)
    
