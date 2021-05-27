import numpy as np
import math
import config as cf
import checking as chk

def getA456(Tx, Ty, Tz, a1, a2, a3, R_36):
    tests = [[0,0,0], [0,0,1], [0,1,0],
            [0,1,1], [1,0,0], [1,0,1],
            [1,1,0], [1,1,1]]
    
    # Check A456
    for i in range(len(tests)):
        a5 = np.arccos( max(-1.0, min(R_36[2][2], 1.0)) )
        a4 = np.arcsin( max(-1.0, min(R_36[1][2] / np.sin(a5), 1.0)) )
        a6 = np.arccos( max(-1.0, min(-R_36[2][0] / np.sin(a5), 1.0)) )
        if (tests[i][0] == 1):
            a4 = np.pi - a4
        if (tests[i][1] == 1):
            a6 = 2*np.pi - a6
        if (tests[i][2] == 1):
            a5 = 2*np.pi - a5
        
        L6_x, L6_y, L6_z = chk.getJointCoordinates([0, a1, a2, a3, a4, a5, a6])[3]
        #print(f'Checking A456: {round(L6_x, 4)}, {round(L6_y, 4)}, {round(L6_z, 4)}')
        if (round(L6_x, 4)==round(Tx, 4)) and (round(L6_y, 4)==round(Ty, 4)) and (round(L6_z, 4)==round(Tz, 4)):
            return a4, a5, a6

    return 0, 0, 0


def getR_06_plane(Tap, Tae, Tar):
    L4_hor = np.cos(Tae)
    Z_dx = L4_hor * np.cos(Tap)
    Z_dy = L4_hor * np.sin(Tap)
    Z_dz = np.sin(Tae)

    Y_dx = Z_dx
    Y_dy = Z_dz
    Y_dz = - Z_dy

    X_dx = Z_dz
    X_dy = Z_dy
    X_dz = - Z_dx

    R_06 = np.array([[X_dx, Y_dx, Z_dx],
            [X_dy, Y_dy, Z_dy],
            [X_dz, Y_dz, Z_dz],])
    
    R_z = np.array([[0.0] * 3 for i in range(3)])
    R_z[2][2] = 1.0
    R_z[0][0] = np.cos(Tar)
    R_z[0][1] = -np.sin(Tar)
    R_z[1][0] = np.sin(Tar)
    R_z[1][1] = np.cos(Tar)
    
    return np.matrix.dot(R_06, R_z)
