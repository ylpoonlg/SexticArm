import numpy as np
import config as cf
import RRR

def getJointCoordinates(a):
    # Link 1
    L1_x, L1_y, L1_z = 0, 0, cf.L1

    # Link 2
    L2_hor = cf.L2 * np.sin(a[2])
    L2_ver = cf.L2 * np.cos(a[2])
    L2_x = L1_x + L2_hor * np.cos(a[1])
    L2_y = L1_y + L2_hor * np.sin(a[1])
    L2_z = L1_z + L2_ver

    # Link 3
    L23 = np.sqrt(pow(cf.L2, 2) + pow(cf.L3, 2) - 2*cf.L2*cf.L3*np.cos(np.pi - a[3]))
    beta = np.arccos((pow(cf.L2, 2) + pow(L23, 2) - pow(cf.L3, 2)) / (2*cf.L2*L23))
    L3_hor = L23 * np.sin(a[2] + beta)
    L3_ver = L23 * np.cos(a[2] + beta)
    L3_x = L1_x + L3_hor * np.cos(a[1])
    L3_y = L1_y + L3_hor * np.sin(a[1])
    L3_z = L1_z + L3_ver

    # Spherical Wrist
    R_03 = RRR.getR_03(a[1], a[2], a[3])

    R_36 = np.array([[0.0] * 3 for i in range(3)])
    R_36[0][0] = np.cos(a[4])*np.cos(a[5])*np.cos(a[6]) - np.sin(a[4])*np.sin(a[6])
    R_36[0][1] = - np.cos(a[4])*np.cos(a[5])*np.sin(a[6]) - np.sin(a[4])*np.cos(a[6])
    R_36[0][2] = np.cos(a[4]) * np.sin(a[5])
    R_36[1][0] = np.sin(a[4])*np.cos(a[5])*np.cos(a[6]) + np.cos(a[5])*np.sin(a[6])
    R_36[1][1] = - np.sin(a[4])*np.cos(a[5])*np.sin(a[6]) + np.cos(a[5])*np.cos(a[6])
    R_36[1][2] = np.sin(a[4]) * np.sin(a[5])
    R_36[2][0] = - np.sin(a[5]) * np.cos(a[6])
    R_36[2][1] = np.sin(a[5]) * np.sin(a[6])
    R_36[2][2] = np.cos(a[5])

    R_06 = np.matrix.dot(R_03, R_36)

    # print('R_03 = ')
    # print(R_03)
    # print('R_36 = ')
    # print(R_36)
    # print('R_06 = ')
    # print(R_06)

    L6_x = L3_x + cf.L4 * R_06[0][2]
    L6_y = L3_y + cf.L4 * R_06[1][2]
    L6_z = L3_z + cf.L4 * R_06[2][2]

    # print(f'J6 (Toolhead): ({round(L6_x, 4)}, {round(L6_y, 4)}, {round(L6_z, 4)})')

    return [(L1_x, L1_y, L1_z),
            (L2_x, L2_y, L2_z),
            (L3_x, L3_y, L3_z),
            (L6_x, L6_y, L6_z),]