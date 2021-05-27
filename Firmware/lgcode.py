import numpy as np
import os
import config as cf
import checking as chk
from functions import *
import RRR, wrist, visualize

class lgcodeRead():
    def __init__(self, script_path):
        super().__init__()
        path = os.path.abspath(script_path)
        print(f'>> Running script at {path}')
        self.script = open(path, 'r')

    def readlns(self):
        # Store current states
        X = 0
        Y = 0
        Z = 0
        P = 0
        E = 0
        R = 0
        F = 200

        lines = self.script.readlines()
        result = []
        for line in lines:
            line = line.split(';')[0]
            line = line.strip('\n')
            cmds = line.split(' ')
            if (len(cmds) == 0):
                continue
            if cmds[0] == 'G0':
                for cmd in cmds:
                    cmd = cmd.strip("\n")
                    if (cmd[0] == 'X'):
                        X = float(cmd[1::])
                    elif (cmd[0] == 'Y'):
                        Y = float(cmd[1::])
                    elif (cmd[0] == 'Z'):
                        Z = float(cmd[1::])
                    elif (cmd[0] == 'P'):
                        P = float(cmd[1::])
                    elif (cmd[0] == 'E'):
                        E = float(cmd[1::])
                    elif (cmd[0] == 'R'):
                        R = float(cmd[1::])
                    elif (cmd[0] == 'F'):
                        F = float(cmd[1::])
                result.append({ 'cmd': 'G0',
                    'X': X, 'Y': Y, 'Z': Z,
                    'P': P, 'E': E, 'R': R,
                    'F': F
                })
            elif cmds[0] == 'G1':
                result.append({ 'cmd': 'G1',
                    'A1': float(cmds[1]), 'A2': float(cmds[2]), 'A3': float(cmds[3]),
                    'A4': float(cmds[4]), 'A5': float(cmds[5]), 'A6': float(cmds[6]),
                    'F': float(cmds[7][1::])
                })


        return result



#-------------------------------------------------------------
#       LGCODE COMMANDS
#-------------------------------------------------------------
def G0(Tx, Ty, Tz, Tap, Tae, Tar, F):
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

    G1(a1, a2, a3, a4, a5, a6, F, unit='rad')

def G1(a1, a2, a3, a4, a5, a6, F, unit='deg'):
    if unit == 'deg':
        a1, a2, a3 = degToRad(a1), degToRad(a2), degToRad(a3)
        a4, a5, a6 = degToRad(a4), degToRad(a5), degToRad(a6)
    
    a = [0, a1, a2, a3, a4, a5, a6]
    a_deg = [0, radToDeg(a1), radToDeg(a2), radToDeg(a3), radToDeg(a4), radToDeg(a5), radToDeg(a6)]
    printA(a_deg, '>> Angles: ')

    J6_x, J6_y, J6_z = chk.getJointCoordinates(a)[3]
    printA([J6_x, J6_y, J6_z], '>> Toolhead: ')
    visualize.show(a)