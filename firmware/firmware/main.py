from firmware.menu import Menu
import firmware.config as cf
from firmware.functions import *
import threading

def init():
    log('''
  ___  ___  ___  ___   ___  ___  ___  ___  ___  
 | __>| . \| . || __> | . \| . || . >| . ||_ _| 
 | . \| | || | || _>  |   /| | || . \| | | | |  
 `___/|___/`___'|_|   |_\_\`___'|___/`___' |_|  
    ''')
    log('                 by ylpoonlg\n')

if (__name__ == '__main__'):
    init()
    Menu()