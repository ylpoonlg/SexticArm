import numpy as np
import math
import firmware.config as cf
import firmware.checking as chk
from firmware.functions import *

def getR_03(a1, a2, a3):
    R_03 = np.array([[0.0] * 3 for i in range(3)])

    R_03[0][0] = np.cos(a1)*np.cos(a2)*np.cos(a3) - np.cos(a1)*np.sin(a2)*np.sin(a3)
    R_03[0][1] = - np.sin(a1)
    R_03[0][2] = np.cos(a1)*np.cos(a2)*np.sin(a3) + np.cos(a1)*np.sin(a2)*np.cos(a3)

    R_03[1][0] = np.sin(a1)*np.cos(a2)*np.cos(a3) - np.sin(a1)*np.sin(a2)*np.sin(a3)
    R_03[1][1] = np.cos(a1)
    R_03[1][2] = np.sin(a1)*np.cos(a2)*np.sin(a3) + np.sin(a1)*np.sin(a2)*np.cos(a3)

    R_03[2][0] = - np.sin(a2)*np.cos(a3) - np.cos(a2)*np.sin(a3)
    R_03[2][1] = 0
    R_03[2][2] = - np.sin(a2)*np.sin(a3) + np.cos(a2)*np.cos(a3)

    log(f'R_03 = \n{R_03}\n', 3)
    return R_03

def getR_36(a4, a5, a6):
    return np.array([
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

def getRotations(a):
    R_03 = getR_03(a[1], a[2], a[3])
    R_36 = getR_36(a[4], a[5], a[6])
    R_06 = np.matrix.dot(R_03, R_36)

    Tae = np.pi/2 - np.arccos(R_06[2][2])
    Tap = np.arccos( R_06[0][2] / np.sin(np.pi/2 - Tae) )

    try:
        a1 = -np.cos(Tap) * np.cos(np.pi/2 - Tae)
        b1 = -np.sin(Tap)
        k1 = R_06[0][1]
        t1 = np.roots([(a1*a1 - k1*k1), (2*a1*b1), (b1*b1 - k1*k1)])
    except:
        t1 = 0
    Tar_1 = [np.arctan(t1[0]), np.arctan(t1[1])]

    try:
        a2 = -np.sin(Tap) * np.cos(np.pi/2 - Tae)
        b2 = np.cos(Tap)
        k2 = R_06[1][1]
        t2 = np.roots([(a2*a2 - k2*k2), (2*a2*b2), (b2*b2 - k2*k2)])
    except:
        t2 = 0
    Tar_2 = [np.arctan(t2[0]), np.arctan(t2[1])]
    
    log(f'getRotations: Tar = {Tar_1}, {Tar_2}', 2)
    if (round(Tar_1[0], 4) == round(Tar_2[0], 4)) or (round(Tar_1[0], 4) == round(Tar_2[1], 4)):
        Tar = Tar_1[0]
    else:
        Tar = Tar_1[1]

    return radToDeg(Tap), radToDeg(Tae), radToDeg(Tar)


def getA123(Wx, Wy, Wz):
    R = np.sqrt(Wx*Wx + Wy*Wy)
    dz = Wz - cf.L1
    L23 = np.sqrt(R*R + dz*dz)

    beta = np.arccos((pow(cf.L2, 2) + pow(L23, 2) - pow(cf.L3, 2)) / (2*cf.L2*L23))
    gamma = np.arccos((pow(cf.L2, 2) + pow(cf.L3, 2) - pow(L23, 2)) / (2*cf.L2*cf.L3))

    # Check sin/cos/tan quadrants
    tests = [[0,0], [1,0], [0,1], [1,1]]
    
    # Check A123
    for i in range(len(tests)):
        alpha = np.pi / 2
        if (R != 0):
            alpha = np.arctan(dz / R)
        a1 = np.pi / 2
        if (round(Wx, 4) != 0):
            a1 = np.arctan(Wy / Wx)
        
        if (tests[i][0] == 1):
            a1 += np.pi
        if (tests[i][1] == 1):
            alpha += np.pi
        
        a2 = np.pi / 2 - alpha - beta
        a3 = np.pi - gamma
        
        L3_x, L3_y, L3_z = chk.getJointCoordinates([0, a1, a2, a3, 0, 0, 0])[2]
        if (round(L3_x, 4)==round(Wx, 4)) and (round(L3_y, 4)==round(Wy, 4)) and (round(L3_z, 4)==round(Wz, 4)):
            if (chk.checkAngleLimits([0, a1, a2, a3, cf.ANGLES_LIMIT[4][0], cf.ANGLES_LIMIT[5][0], cf.ANGLES_LIMIT[6][0]])):
                if (a1 < 0):
                    a1 += 2*np.pi
                if (a2 < 0):
                    a2 += 2*np.pi
                if (a3 < 0):
                    a3 += 2*np.pi
                return a1, a2, a3
    
    log('>> Error: Failed to get a1, a2, a3', 1)
    return -1, -1, -1

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

        test_36 = getR_36(a4, a5, a6)

        if (round(L6_x, 4)==round(Tx, 4)) and (round(L6_y, 4)==round(Ty, 4)) and (round(L6_z, 4)==round(Tz, 4)):
            if round(test_36[0][1], 4) == round(R_36[0][1], 4):
                if (chk.checkAngleLimits([0, cf.ANGLES_LIMIT[1][0], cf.ANGLES_LIMIT[2][0], cf.ANGLES_LIMIT[3][0], a4, a5, a6])):
                    if (a4 < 0):
                        a4 += 2*np.pi
                    if (a5 < 0):
                        a5 += 2*np.pi
                    if (a6 < 0):
                        a6 += 2*np.pi
                    return a4, a5, a6

    log('>> Error: Failed to get a4, a5, a6', 1)
    return -1, -1, -1

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

    a1, a2, a3 = getA123(Wx, Wy, Wz)
    R_03 = getR_03(a1, a2, a3)
    R_03_inv = np.linalg.inv(R_03)
    R_36 = np.matrix.dot(R_03_inv, R_06)
    log(f'R_36 = \n{R_36}\n', 3)

    a4, a5, a6 = getA456(Tx, Ty, Tz, a1, a2, a3, R_36)

    if (a1 == -1) or (a4 == -1):
        return -1, -1, -1, -1, -1, -1

    return a1, a2, a3, a4, a5, a6