import numpy as np
import os
import firmware.config as cf
import firmware.checking as chk
from firmware.functions import *
import firmware.ik as ik
import firmware.visualize as visualize
import firmware.robot as robot

class lgcodeReader():
    def __init__(self):
        self.status = {
            'X': 0, 'Y': 0, 'Z': cf.L1 + cf.L2 + cf.L3 + cf.L4,
            'P': 0, 'E': 90, 'R': 0,
            'A1': 0, 'A2': 0, 'A3': 0,
            'A4': 0, 'A5': 0, 'A6': 0,
            'F': cf.DEFAULT_FEEDRATE,
        }

    def decExeCommand(self, cmd):
        cmd = cmd.split(';')[0].strip('\n').upper()
        log(f'Command Received: {cmd}')
        paramtrs = cmd.split(' ')
        if (len(paramtrs) == 0):
            return
        
        if (paramtrs[0] == 'G0'):
            for p in paramtrs:
                if (p[0] == 'A'):
                    instr = p[0:2]
                    op = float(p[2::])
                    self.status[instr] = degToRad(op)

            G0( self.status['A1'], self.status['A2'], self.status['A3'],
                self.status['A4'], self.status['A5'], self.status['A6'],
                self.status['F'] )

            # Update position as well
            a = [0, self.status['A1'], self.status['A2'], self.status['A3'],
                    self.status['A4'], self.status['A5'], self.status['A6']]
            X, Y, Z = chk.getJointCoordinates(a)[3]
            self.status['X'], self.status['Y'], self.status['Z'] = X, Y, Z
            
            
        elif (paramtrs[0] == 'G1'):
            for p in paramtrs:
                op = float(p[1::])
                self.status[p[0]] = op
            G1( self.status['X'], self.status['Y'], self.status['Z'],
                self.status['P'], self.status['E'], self.status['R'],
                self.status['F'] )

            # Update angles as well
            a = ik.getAngles( self.status['X'], self.status['Y'], self.status['Z'],
                              self.status['P'], self.status['E'], self.status['R'])

            self.status['A1'], self.status['A2'] = a[0], a[1]
            self.status['A3'], self.status['A4'] = a[2], a[3]
            self.status['A5'], self.status['A6'] = a[4], a[5]
            

    def readFile(self, path):
        path = os.path.abspath(path)
        log(f'>> Running script at {path}...', 0)
        script = open(path, 'r')
        lines = script.readlines()
        log('________STARTING________', 0)
        for line in lines:
            self.decExeCommand(line)
        log('________FINISHED________\n', 0)



#-------------------------------------------------------------
#       LGCODE COMMANDS
#-------------------------------------------------------------
def G0(a1, a2, a3, a4, a5, a6, F):
    a = [0, a1, a2, a3, a4, a5, a6]
    a_deg = [radToDeg(a1), radToDeg(a2), radToDeg(a3), radToDeg(a4), radToDeg(a5), radToDeg(a6)]
    printA(a_deg, '>> Angles: ')
    J6_x, J6_y, J6_z = chk.getJointCoordinates(a)[3]
    printA([J6_x, J6_y, J6_z], '>> Toolhead: ')

    robot.move(a)

    # visualize.show(a)

def G1(Tx, Ty, Tz, Tap, Tae, Tar, F):
    Tap, Tae, Tar = degToRad(Tap), degToRad(Tae), degToRad(Tar) # convert to radian
    a1, a2, a3, a4, a5, a6 = ik.getAngles(Tx, Ty, Tz, Tap, Tae, Tar)
    G0(a1, a2, a3, a4, a5, a6, F)
