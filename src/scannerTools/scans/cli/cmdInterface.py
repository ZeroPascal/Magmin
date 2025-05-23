 
import platform
import subprocess
from definitions import ROOT_DIR
import os


def prepPaths(filePath:str, sub='', exe='ffprobe'):
    root =''
    try:
        if(platform.system() != 'Windows'):
            
                filePath = filePath.replace(' ','\ ')
                if(exe):
                    root = os.path.join(ROOT_DIR,'bin',exe)
                else:
                    root = os.path.join(ROOT_DIR,'bin',sub)
                root = root.replace(' ','\ ')
        if(platform.system() == 'Windows'):
                filePath = filePath.replace(' ','` ')
                filePath = '"'+filePath+'"'
                if(exe):
                    root = os.path.join(ROOT_DIR,'bin',sub,exe+'.exe')
                else:
                    root = os.path.join(ROOT_DIR,'bin',sub)
                root = root.replace(' ','` ')
    except:
         pass

    return (root,filePath)

def cmdInterface(cmd:str,timeout=5):
    """Takes a CLI Command as a string, returns outputs"""
    try:
        if(platform.system() == 'Windows'):
            p= runWindows(cmd)
        else:
            p = runUnix(cmd)

        out = p.communicate(timeout=timeout)   
     #   print('Job Started')
        if not p.poll() or out[1]:
      #      print('     Job done',cmd)
            stop = True
            
            return out[0]+out[1] 
        else:
            print('     Job Cancled')
        
    except Exception as e:
            print('Run Got Error',str(e))
            stop = True
        
            if(type(e)== subprocess.TimeoutExpired):
                return 'Error: Timeout'
            return e
def runUnix(cmd):
    return subprocess.Popen([cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True,shell=True)

def runWindows(cmd):
    
     return subprocess.Popen(['powershell',cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE,  stdin=subprocess.PIPE, text=True, shell=True)