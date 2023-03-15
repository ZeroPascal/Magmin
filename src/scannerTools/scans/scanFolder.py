import datetime
import os
import platform
from pathlib import Path, PosixPath
from scannerDatabase import *
import scannerActions as actions
from .ffmpegScan import ffmpegScan
import pprint
ignoreExtenstions:list[str] = []#['.txt']
def checkExtenstion(ex:str)->bool:
    try:
        return ignoreExtenstions.index(ex) == 0
    except:
        return True

#https://stackoverflow.com/questions/55638905/how-to-convert-os-stat-result-to-a-json-that-is-an-object
def stat_to_json(s_obj) -> dict:
    return {k: getattr(s_obj, k) for k in dir(s_obj) if k.startswith('st_')}

def processFile(file):
    file['lastAction']=''
    try:

        f = scannerDB.files.getFileByID(file['st_ino'])
                #print('Found File with same st_ino',f)
        if f:
                    #print('     File Already Exists')
                    
            if f and f.name != file['name']:
                print('Name Change:',file['name'])
                file['lastAction']= 'Name Change'
                #new_files.append(file)
            if f and f.st_mtime != file['st_mtime']:
                print('Modified',file['name'], type(f.st_mtime), type(file['st_mtime']))
                file['lastAction']='Modified'
        else:
                #    print('Issuse:',file['name'])
            raise 'New File'
    except Exception as e:
        print('     New Or Modified File',file['root']+file['name'])
        f= scannerDB.files.getFileByName_Path(path=file['root'],name=file['name'])
        print(f)
        if f:
            print(f)
            file['lastAction']='Modified'
        else:
            file['lastAction']='New'
    
    try:
            file.pop('st_file_attributes')
    except:
            pass
    try:
            file.pop('st_reparse_tag')
    except:
            pass
    try:
            file.pop('st_blksize')
    except:
            pass
    try:
            file.pop('st_blocks')
    except Exception as e:
            print('Scan Error',e)
    if platform.system()=='Windows':
            file['st_birthtime'] =file['st_ctime']
   # if(file['lastAction']=='New' or file['lastAction']=='Modified'):           
    try:
            file.update(ffmpegScan(str(file['path'])))
        
    except Exception as e:
            print('FFProbe Error',e)
    return file

def processScan(folder,files):
    known_children = scannerDB.files.getFilesFromFolder(folder['root'])
   
    new_files = []
    
    for file in files:
        
        file = processFile(file)
        try:
            known_children.remove(file['st_ino'])
        except:
            pass
            
        new_files.append(file)

      #  print('File ',file['name'],file['lastAction'])
    if len(new_files)==0 and len(known_children) ==0:
        print('No Changes to:',folder['name'])

    scannerDB.files.addFiles(new_files)
    scannerDB.files.removeFiles(known_children)
   # print(known_children)
                     

def scanFolder(folder:Folder):
    files =[]
    path = Path(folder['root'])

    if path.exists():
        print('Scanning Folder',folder['root'])
        for child in path.iterdir():
            if child.is_file() and checkExtenstion(child.suffix):
                j = stat_to_json(os.stat(child))
                j['name'] = child.name
                j['root'] = folder['root']
                j['path'] = child.absolute()
                files.append(j)
        

        processScan(folder,files)
        actions.updateDirectoryScanTime(folder['name'],datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        print('Scanning Folder Done')
    else:
        print('No Such Path',path)
    
