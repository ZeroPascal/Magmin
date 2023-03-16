#from scannerDatabase import ScannerDatabase, scannerDB
import sys
from dotenv import load_dotenv
from scannerServer import start_server
import os

if __name__ == '__main__': 
    print('Starting Magmin')
    #https://github.com/theskumar/python-dotenv/issues/259#issuecomment-951203812
    extDataDir = os.getcwd()
    if getattr(sys, 'frozen', False):
        extDataDir = sys._MEIPASS
    load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

    print('CWD',os.getcwd())

    start_server(os.getenv('SERVER_SECRET'))
    