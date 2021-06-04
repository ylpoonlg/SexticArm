import numpy as np
import firmware.config as cf

OUTPUT_FILE_PATH = './outputConsole.txt'
OUTPUT_LINES_LIMIT = 50

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
        # Log to file
        file = open(OUTPUT_FILE_PATH, 'r')
        lines = file.readlines()
        if (len(lines) >= OUTPUT_LINES_LIMIT):
            lines.pop(0)
        file = open(OUTPUT_FILE_PATH, 'w+')
        file.writelines(lines)
        file.write(f'{msg}\n')

        print(msg)

def getConsole():
    file = open(OUTPUT_FILE_PATH, 'r')
    return file.read()

def clearConsole():
    file = open(OUTPUT_FILE_PATH, 'w')
    file.write('')