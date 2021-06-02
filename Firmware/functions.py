import numpy as np
import config as cf

# Functions
def degToRad(a):
    return a * np.pi / 180.0

def radToDeg(a):
    return a * 180.0 / np.pi

def printA(a, msg):
    a_tmp = []
    for i in range(len(a)):
        a_tmp.append(round(a[i], 4))
    print(f'{msg}{a_tmp}')

def log(msg, lvl=0):
    if cf.DEBUG_LOG_LEVEL >= lvl:
        print(msg)