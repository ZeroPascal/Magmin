#from scannerDatabase import ScannerDatabase, scannerDB
from dotenv import load_dotenv
from scannerServer import start_server
import os

if __name__ == '__main__': 
    print('Starting Magmin')
    load_dotenv() 
    start_server(os.getenv('SERVER_SECRET'))
    