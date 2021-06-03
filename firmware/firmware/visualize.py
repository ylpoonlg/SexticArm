import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import firmware.checking as chk

fig = None
ax = None

# Init
def init():
    global fig, ax
    fig = plt.figure()
    ax = plt.axes(projection ='3d')

def plotLine(S, E, clr='black'):
    global ax
    ax.plot([S[0], E[0]], [S[1], E[1]], [S[2], E[2]], color=clr)

# Plot
def show(a):
    global fig, ax

    J_coor = chk.getJointCoordinates(a)
    (L1_x, L1_y, L1_z) = J_coor[0]
    (L2_x, L2_y, L2_z) = J_coor[1]
    (L3_x, L3_y, L3_z) = J_coor[2]
    (L6_x, L6_y, L6_z) = J_coor[3]

    plotLine([0, 0, 0],          [L1_x, L1_y, L1_z], '#ff0000')
    plotLine([L1_x, L1_y, L1_z], [L2_x, L2_y, L2_z], '#ff9300')
    plotLine([L2_x, L2_y, L2_z], [L3_x, L3_y, L3_z], '#00ff22')
    plotLine([L3_x, L3_y, L3_z], [L6_x, L6_y, L6_z], '#0022ff')

    # Show
    ax.set_title('6DOF visual')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    ax.set_xlim3d(-200, 200)
    ax.set_ylim3d(-200, 200)
    ax.set_zlim3d(0, 350)

    plt.show(block=False)