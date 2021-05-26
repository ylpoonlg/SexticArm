# Libraries
import numpy as np
import math

# Modules
import config as cf
import RRR
import wrist
import checking as chk
import visualize

# Functions
def degToRad(a):
    return a * np.pi / 180.0

def radToDeg(a):
    return a * 180.0 / np.pi

def printA(a, msg):
    A_tmp = [
        round(radToDeg(a[1]), 4),
        round(radToDeg(a[2]), 4),
        round(radToDeg(a[3]), 4),
        round(radToDeg(a[4]), 4),
        round(radToDeg(a[5]), 4),
        round(radToDeg(a[6]), 4),
    ]
    print(f'{msg}{A_tmp}')
    print()

def printMatrix(M, msg):
    print(f'{msg}{M}')
    print()

def getAngles():
    # Get Target
    Tx , Ty, Tz = cf.Tx, cf.Ty, cf.Tz
    R_06 = None
    if (cf.ANGLE_MODE == "legacy"):
        Tax, Tay, Taz = degToRad(cf.Tax), degToRad(cf.Tay), degToRad(cf.Taz) # convert to radian
        R_06 = wrist.getR_06_legacy(Tax, Tay, Taz)
    elif (cf.ANGLE_MODE == "plane"):
        Tap, Tae, Tar = degToRad(cf.Tap), degToRad(cf.Tae), degToRad(cf.Tar) # convert to radian
        R_06 = wrist.getR_06_plane(Tap, Tae, Tar)

    # Get W (Position of the spherical wrist)
    Wx = Tx - R_06[0][2] * cf.L4
    Wy = Ty - R_06[1][2] * cf.L4
    Wz = Tz - R_06[2][2] * cf.L4

    print(f'W ({Wx}, {Wy}, {Wz})')
    print()

    a1, a2, a3 = RRR.getA123(Wx, Wy, Wz)

    R_03 = RRR.getR_03(a1, a2, a3)
    R_03_inv = np.linalg.inv(R_03)
    R_36 = np.matrix.dot(R_03_inv, R_06)

    a4, a5, a6 = wrist.getA456(a1, a2, a3, R_36)
    return a1, a2, a3, a4, a5, a6

def init():
    print('''
  ___  ___  ___  ___   ___  ___  ___  ___  ___  
 | __>| . \| . || __> | . \| . || . >| . ||_ _| 
 | . \| | || | || _>  |   /| | || . \| | | | |  
 `___/|___/`___'|_|   |_\_\`___'|___/`___' |_|  
    ''')
    print('                 by ylpoonlg\n')

def main():
    a1, a2, a3, a4, a5, a6 = getAngles()
    printA([0, a1, a2, a3, a4, a5, a6], 'A')
    visualize.show([0, a1, a2, a3, a4, a5, a6])

if (__name__ == '__main__'):
    init()
    main()