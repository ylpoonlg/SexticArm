import numpy as np

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