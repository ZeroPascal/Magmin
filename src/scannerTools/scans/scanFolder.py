import datetime
import os
import platform
from pathlib import Path, PosixPath
from scannerDatabase import *
import scannerActions as actions
from definitions import THUMBNAIL_DIR
from .ffmpegScan import ffmpegScan
import pprint
ignoreExtenstions:list[str] = []#['.txt']
def checkExtenstion(ex:str,exList:list[str]=ignoreExtenstions)->bool:
    try:
        return exList.index(ex) == 0
    except:
        return True

probeExtenstions=['.mov','.jpg']


#https://stackoverflow.com/questions/55638905/how-to-convert-os-stat-result-to-a-json-that-is-an-object
def stat_to_json(s_obj) -> dict:
    return {k: getattr(s_obj, k) for k in dir(s_obj) if k.startswith('st_')}

def processFile(file):
    try:

        f = scannerDB.files.getFileByID(file['st_ino'])
        #print('Found File with same st_ino',f)
        if f:
         #   print('     File Already Exists')
                    
            if(f['name'] != file['name']):
                print('Name Change:',file['name'])
                file['lastAction']= 'Name Change'
                #new_files.append(file)
            elif(f['st_mtime'] != file['st_mtime']):
                print('Modified',file['name'], type(f.st_mtime), type(file['st_mtime']))
                file['lastAction']='Modified'
            else:
                 file['lastAction']=''
        else:
            print('Issuse:',file['name'])
            raise 'New File'
    except Exception as e:
        print('     New Or Modified File',file['root']+file['name'])
        f= scannerDB.files.getFileByName_Path(path=file['root'],name=file['name'])
        if f:
          #  print(f)
            file['lastAction']='Modified'
        else:
            file['lastAction']='New'
    #Removes stats that are OSX only
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
            pass
    if platform.system()=='Windows':
            file['st_birthtime'] =file['st_ctime']  
    try:    
           # pprint.pprint(file)          
            if(file['lastAction'] == 'New' or file['lastAction'] == 'Modified'):
                file.update(ffmpegScan(str(file['path']),file['st_ino']))
        
    except Exception as e:
            print('FFProbe Error',e)
    return file

def processScan(folder,files):
    known_children = scannerDB.files.getFilesFromFolder(folder['root'])
    new_files = []
    
    for file in files:
        file = processFile(file)

       # pprint.pprint(updatedFile)
        try:
            known_children.remove(file['st_ino'])
            oldFile = scannerDB.files.getFileByID(file['st_ino'])
            oldFile.update(file)
            file= oldFile
          #  file.update(file)
        except:
            pass
        new_files.append(file)
  #  print(len(new_files),len(known_children))
    if len(new_files)==0 and len(known_children) ==0:
        print('No Changes to:',folder['name'])

    for deletedFile in known_children:
        try:
       #     print(deletedFile)
            os.remove(os.path.join(THUMBNAIL_DIR,str(deletedFile)+'_thumb.png'))
        except:
            pass

    scannerDB.files.addFiles(new_files)
    scannerDB.files.removeFiles(known_children)
   # print(known_children)
                     

def checkHidden(file:str)->bool:
    if platform.system() == 'Windows':
        import ctypes
        attribute = ctypes.windll.kernel32.GetFileAttributesW(file)
        return not attribute & 2  # FILE_ATTRIBUTE_HIDDEN
    else:
         return not os.path.basename(file).startswith('.')

def scanFolder(folder:Folder):
    files =[]
    path = Path(folder['root'])

    if path.exists():
        print('Scanning Folder',folder['root'])
        for child in path.iterdir():
            if child.is_file() and checkExtenstion(child.suffix) and checkHidden(child):
                j = stat_to_json(os.stat(child))
                j['name'] = child.name
                j['root'] = folder['root']
                j['path'] = child.absolute()
                j['suffix'] =child.suffix
                files.append(j)
        

        processScan(folder,files)
        actions.updateDirectoryScanTime(folder['name'],datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        print('Scanning Folder Done')
    else:
        print('No Such Path',path)
    
