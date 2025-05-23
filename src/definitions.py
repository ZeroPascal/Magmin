import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if getattr(sys, 'frozen', False):
    EXE_DIR = os.getcwd()
else:    
    EXE_DIR = os.path.dirname(os.path.abspath(__file__))


THUMBNAIL_DIR = os.path.join(ROOT_DIR,'scannerServer','thumbnails')