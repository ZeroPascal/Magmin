
import json
import os
from pathlib import Path
import platform
import subprocess

from definitions import ROOT_DIR


def ffmpegScan(filePath:str):
    info =json.loads(scan(filePath))
    print(info)


def scan(filePath:str):
    print(filePath)
    try:
        root = os.path.join(ROOT_DIR,'bin','ffprobe.exe')
       # cmd = Path(cmd)
      #  path = Path(filePath)
        if(platform.system() != 'Windows'):
            filePath = filePath.replace(' ','\ ')
            root = root.replace(' ','\ ')
        if(platform.system() == 'Windows'):
            filePath = filePath.replace(' ','` ')
            root = root.replace(' ','` ')
        cmd=''+root+' -v error -print_format json -select_streams v:0 -show_entries stream=height,width -i "'+filePath+'"'
        if(platform.system() == 'Windows'):
            p= runWindows(cmd)
        else:
            p = runUnix(cmd)

        out = p.communicate(timeout=3)   
        print('Job Started')
        if not p.poll() or out[1]:
                print('     Job done',cmd)
                stop = True
           
                return out[0] #+out[1] 
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