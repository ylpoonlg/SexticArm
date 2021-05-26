import numpy as np
import config as cf
import checking as chk

def getA456(a1, a2, a3, R_36):

    tests = [[0,0,0], [0,0,1], [0,1,0],
            [0,1,1], [1,0,0], [1,0,1],
            [1,1,0], [1,1,1]]

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

        print(f'Checking A456: {round(L6_x, 4)}, {round(L6_y, 4)}, {round(L6_z, 4)}')

        if (round(L6_x, 4)==round(cf.Tx, 4)) and (round(L6_y, 4)==round(cf.Ty, 4)) and (round(L6_z, 4)==round(cf.Tz, 4)):
            return a4, a5, a6

    return 0, 0, 0
