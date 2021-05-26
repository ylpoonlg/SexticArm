# Libraries
import numpy as np
import math

# Modules
import config as cf
import RRR
import wrist
import checking as chk
import visualize

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

def getR_06(ax, ay, az):
       R_x = np.array([[0.0] * 3 for i in range(3)])
       R_y = np.array([[0.0] * 3 for i in range(3)])
       R_z = np.array([[0.0] * 3 for i in range(3)])

       R_x[0][0] = 1.0
       R_x[1][1] = np.cos(ax)
       R_x[1][2] = -np.sin(ax)
       R_x[2][1] = np.sin(ax)
       R_x[2][2] = np.cos(ax)

       R_y[1][1] = 1.0
       R_y[0][0] = np.cos(ay)
       R_y[2][0] = -np.sin(ay)
       R_y[0][2] = np.sin(ay)
       R_y[2][2] = np.cos(ay)

       R_z[2][2] = 1.0
       R_z[0][0] = np.cos(az)
       R_z[0][1] = -np.sin(az)
       R_z[1][0] = np.sin(az)
       R_z[1][1] = np.cos(az)

       R_06 = np.matrix.dot(np.matrix.dot(R_x, R_y), R_z)
       return R_06

# Init
x0, y0, z0 = 0, 0, 0

# Main
# Set Target
Tx , Ty, Tz = cf.Tx, cf.Ty, cf.Tz
Tax, Tay, Taz = degToRad(cf.Tax), degToRad(cf.Tay), degToRad(cf.Taz) # convert to radian

R_06 = getR_06(Tax, Tay, Taz)
# print("R_06 =")
# print(R_06)
# print()

# Get W (Position of the spherical wrist)
Wx = Tx - R_06[0][2] * cf.L4
Wy = Ty - R_06[1][2] * cf.L4
Wz = Tz - R_06[2][2] * cf.L4

print(f'W({Wx}, {Wy}, {Wz})')
print()

a1, a2, a3 = RRR.getA123(Wx, Wy, Wz)

R_03 = RRR.getR_03(a1, a2, a3)
# print("R_03 = ")
# print(R_03)
# print()

R_03_inv = np.linalg.inv(R_03)
R_36 = np.matrix.dot(R_03_inv, R_06)
# print('R_36 = ')
# print(R_36)
# print()

a4, a5, a6 = wrist.getA456(a1, a2, a3, R_36)

printA([0, a1, a2, a3, a4, a5, a6], 'A')
print()
visualize.show([0, a1, a2, a3, a4, a5, a6]) # First value is a dummy value