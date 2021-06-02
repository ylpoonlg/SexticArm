import numpy as np
import config as cf
import checking as chk
from functions import *

def getA123(Wx, Wy, Wz):
    R = np.sqrt(Wx*Wx + Wy*Wy)
    dz = Wz - cf.L1
    L23 = np.sqrt(R*R + dz*dz)

    alpha = np.pi / 2
    if (R != 0):
        alpha = np.arctan(dz / R)
    beta = np.arccos((pow(cf.L2, 2) + pow(L23, 2) - pow(cf.L3, 2)) / (2*cf.L2*L23))
    gamma = np.arccos((pow(cf.L2, 2) + pow(cf.L3, 2) - pow(L23, 2)) / (2*cf.L2*cf.L3))

    a1, a2, a3 = checkA123(Wx, Wy, Wz, alpha, beta, gamma)
    return a1, a2, a3

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

def checkA123(Wx, Wy, Wz, alpha, beta, gamma):
    a1_ori = np.pi / 2
    if (round(Wx, 4) != 0):
        a1_ori = np.arctan(Wy / Wx)

    tests = [[0,0], [1,0], [0,1], [1,1]]

    for i in range(len(tests)):
        a1 = a1_ori + np.pi * tests[i][0]
        a2 = np.pi/2.0 - (alpha + np.pi * tests[i][1]) - beta
        a3 = np.pi - gamma

        L3_x, L3_y, L3_z = chk.getJointCoordinates([0, a1, a2, a3, 0, 0, 0])[2]

        if (round(L3_x, 4)==round(Wx, 4)) and (round(L3_y, 4)==round(Wy, 4)) and (round(L3_z, 4)==round(Wz, 4)):
            if (a1 < 0):
                a1 += 2*np.pi
            if (a2 < 0):
                a2 += 2*np.pi
            if (a3 < 0):
                a3 += 2*np.pi
            return a1, a2, a3

    return 0, 0, 0