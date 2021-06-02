import numpy as np
import math
import config as cf
import checking as chk
from functions import *
import RRR

def getA456(Tx, Ty, Tz, a1, a2, a3, R_36):
    # Check sin/cos/tan quadrants
    tests = [[0,0,0], [0,0,1], [0,1,0],
            [0,1,1], [1,0,0], [1,0,1],
            [1,1,0], [1,1,1]]
    
    # Check A456
    for i in range(len(tests)):
        a5 = np.arccos( max(-1.0, min(R_36[2][2], 1.0)) )
        a4, a6 = 0, 0
        if (round(np.sin(a5), 4) == 0):
            a4 = 0
            a6 = np.arccos(R_36[0][0])
        else:
            a4 = np.arcsin( max(-1.0, min(R_36[1][2] / np.sin(a5), 1.0)) )
            a6 = np.arccos( max(-1.0, min(-R_36[2][0] / np.sin(a5), 1.0)) )
        
        if (tests[i][0] == 1):
            a4 = np.pi - a4
        if (tests[i][1] == 1):
            a6 = 2*np.pi - a6
        if (tests[i][2] == 1):
            a5 = 2*np.pi - a5
        
        L6_x, L6_y, L6_z = chk.getJointCoordinates([0, a1, a2, a3, a4, a5, a6])[3]

        test_36 = np.array([
            [np.cos(a4)*np.cos(a5)*np.cos(a6) - np.sin(a4)*np.sin(a6),
            -np.cos(a4)*np.cos(a5)*np.sin(a6) - np.sin(a4)*np.cos(a6),
            np.cos(a4)*np.sin(a5)],
            [np.sin(a4)*np.cos(a5)*np.cos(a6) + np.cos(a4)*np.sin(a6),
            -np.sin(a4)*np.cos(a5)*np.sin(a6) + np.cos(a4)*np.cos(a6),
            np.sin(a4)*np.sin(a5)],
            [-np.sin(a5)*np.cos(a6),
            np.sin(a5)*np.sin(a6),
            np.cos(a5)]
        ])

        if (round(L6_x, 4)==round(Tx, 4)) and (round(L6_y, 4)==round(Ty, 4)) and (round(L6_z, 4)==round(Tz, 4)):
            if round(test_36[0][1], 4) == round(R_36[0][1], 4):
                if (a4 < 0):
                    a4 += 2*np.pi
                if (a5 < 0):
                    a5 += 2*np.pi
                if (a6 < 0):
                    a6 += 2*np.pi
                return a4, a5, a6

    return 0, 0, 0


def getR_06_plane(Tap, Tae, Tar):
    Tae = np.pi/2 - Tae
    R_06 = np.array([
            [np.cos(Tap)*np.cos(Tae)*np.cos(Tar) - np.sin(Tap)*np.sin(Tar),
            -np.cos(Tap)*np.cos(Tae)*np.sin(Tar) - np.sin(Tap)*np.cos(Tar),
            np.cos(Tap)*np.sin(Tae)],
            [np.sin(Tap)*np.cos(Tae)*np.cos(Tar) + np.cos(Tap)*np.sin(Tar),
            -np.sin(Tap)*np.cos(Tae)*np.sin(Tar) + np.cos(Tap)*np.cos(Tar),
            np.sin(Tap)*np.sin(Tae)],
            [-np.sin(Tae)*np.cos(Tar),
            np.sin(Tae)*np.sin(Tar),
            np.cos(Tae)]
        ])
    
    log(f'R_06 = \n{R_06}\n', 3)

    return R_06

def getWristPosition(Tx, Ty, Tz, Tap, Tae, Tar):
    R_06 = getR_06_plane(Tap, Tae, Tar)

    Wx = Tx - R_06[0][2] * cf.L4
    Wy = Ty - R_06[1][2] * cf.L4
    Wz = Tz - R_06[2][2] * cf.L4
    log(f'W ({Wx}, {Wy}, {Wz})', 2)

    return Wx, Wy, Wz

def getAngles(Tx, Ty, Tz, Tap, Tae, Tar):
    R_06 = getR_06_plane(Tap, Tae, Tar)
    Wx, Wy, Wz = getWristPosition(Tx, Ty, Tz, Tap, Tae, Tar)

    a1, a2, a3 = RRR.getA123(Wx, Wy, Wz)
    R_03 = RRR.getR_03(a1, a2, a3)
    R_03_inv = np.linalg.inv(R_03)
    R_36 = np.matrix.dot(R_03_inv, R_06)
    log(f'R_36 = \n{R_36}\n', 3)

    a4, a5, a6 = getA456(Tx, Ty, Tz, a1, a2, a3, R_36)

    return a1, a2, a3, a4, a5, a6