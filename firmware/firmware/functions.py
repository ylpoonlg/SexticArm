import numpy as np
import firmware.config as cf

# Functions
def degToRad(a):
    return a * np.pi / 180.0

def radToDeg(a):
    return a * 180.0 / np.pi

def printA(a, msg):
    a_tmp = []
    for i in range(len(a)):
        a_tmp.append(round(a[i], 4))
    log(f'{msg}{a_tmp}', 0)

def log(msg, lvl=0):
    global outputConsole
    if cf.DEBUG_LOG_LEVEL >= lvl:
        file = open('./outputConsole.txt', 'a')
        file.write(f'{msg}\n')
        print(msg)

def getConsole():
    file = open('./outputConsole.txt', 'r')
    return file.read()

def clearConsole():
    file = open('./outputConsole.txt', 'w')
    file.write('')