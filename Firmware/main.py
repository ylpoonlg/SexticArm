# Libraries
import numpy as np
import math

# Modules
import config as cf
import RRR
import wrist
import checking as chk
import visualize
import lgcode
from functions import *


# Input target: angles in degrees
def getAngles(Tx, Ty, Tz, Tap, Tae, Tar):
    Tap, Tae, Tar = degToRad(Tap), degToRad(Tae), degToRad(Tar) # convert to radian
    R_06 = wrist.getR_06_plane(Tap, Tae, Tar)

    # Get W (Position of the spherical wrist)
    Wx = Tx - R_06[0][2] * cf.L4
    Wy = Ty - R_06[1][2] * cf.L4
    Wz = Tz - R_06[2][2] * cf.L4

    # print(f'W ({Wx}, {Wy}, {Wz})')

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
        print('\n________Ready________\n')
        
        opt = input('Press Enter to start (q to exit) ')
        if (opt == 'q'):
            break

        # read lgcode
        script_file_name = 'test.lgcode'
        if (cf.SCRIPT_FOLDER_PATH[-1] != '/'):
            script_file_name = '/' + script_file_name
        reader = lgcode.lgcodeRead(cf.SCRIPT_FOLDER_PATH+script_file_name)

        # parse commands from file
        cmds = reader.readlns()

        print('>> Starting')
        visualize.init() # New display window
        for cmd in cmds:
            print('-------------------')
            if (cmd['cmd'] == 'G0'):
                lgcode.G0(cmd['A1'], cmd['A2'], cmd['A3'], cmd['A4'], cmd['A5'], cmd['A6'], cmd['F'])
            elif (cmd['cmd'] == 'G1'):
                lgcode.G1(cmd['X'], cmd['Y'], cmd['Z'], cmd['P'], cmd['E'], cmd['R'], cmd['F'])
                
        print('\n________Finished________\n')

if (__name__ == '__main__'):
    init()
    main()