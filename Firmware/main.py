# Libraries
import numpy as np
import math

# Modules
import config as cf
import RRR
import wrist
import checking as chk
import visualize
from lgcode import lgcodeRead

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

def printList(M, msg):
    print(msg)
    print(M)
    print()

# Input target: angles in degrees
def getAngles(Tx, Ty, Tz, Tap, Tae, Tar):
    Tap, Tae, Tar = degToRad(Tap), degToRad(Tae), degToRad(Tar) # convert to radian
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

    a4, a5, a6 = wrist.getA456(Tx, Ty, Tz, a1, a2, a3, R_36)
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
    while True:
        print('...Ready...')
        
        opt = input('Press Enter to start (q to exit) ')
        if (opt == 'q'):
            break

        # read lgcode
        script_file_name = 'test.lgcode'
        if (cf.SCRIPT_FOLDER_PATH[-1] != '/'):
            script_file_name = '/' + script_file_name
        reader = lgcodeRead(cf.SCRIPT_FOLDER_PATH+script_file_name)

        # parse commands from file
        cmds = reader.readlns()
        printList(cmds, 'LGCODE commands: ')

        print('>> Starting')
        for cmd in cmds:
            print('-------------------')
            if(cmd['cmd'] == 'G0'):
                a1, a2, a3, a4, a5, a6 = getAngles(cmd['X'], cmd['Y'], cmd['Z'], cmd['P'], cmd['E'], cmd['R'])
                printA([0, a1, a2, a3, a4, a5, a6], 'A')
                visualize.show([0, a1, a2, a3, a4, a5, a6])
        print('________Finished_________\n')

if (__name__ == '__main__'):
    init()
    main()