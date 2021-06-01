# Libraries
import numpy as np
import math
import os

# Modules
import config as cf
import RRR
import wrist
import checking as chk
import visualize
import lgcode
from menu import Menu
from functions import *

def init():
    print('''
  ___  ___  ___  ___   ___  ___  ___  ___  ___  
 | __>| . \| . || __> | . \| . || . >| . ||_ _| 
 | . \| | || | || _>  |   /| | || . \| | | | |  
 `___/|___/`___'|_|   |_\_\`___'|___/`___' |_|  
    ''')
    print('                 by ylpoonlg\n')


if (__name__ == '__main__'):
    init()
    Menu()