import numpy as np
import os, time
import firmware.config as cf
import firmware.checking as chk
from firmware.functions import *
import firmware.ik as ik
import firmware.visualize as visualize
import serial
import threading

class lgcodeReader():
    def __init__(self, port='/dev/ttyACM0'):
        # everything in degrees
        self.status = {
            'X': 0, 'Y': 0, 'Z': cf.L1 + cf.L2 + cf.L3 + cf.L4,
            'P': 0, 'E': 90, 'R': 0,
            'A1': 0, 'A2': 0, 'A3': 0,
            'A4': 0, 'A5': 0, 'A6': 0,
            'F': cf.DEFAULT_FEEDRATE,
            'serial': False,
            'joints': []
        }

        self.cmdQueue = []
        
        threading.Thread(target=self.run).start()

    def getStatus(self):
        # Update serial connection status
        try:
            if self.ser.isOpen():
                self.status['serial'] = True
            else:
                self.status['serial'] = False
        except:
            self.status['serial'] = False
        
        # Calculate joint positions
        a = [0, degToRad(self.status['A1']), degToRad(self.status['A2']), degToRad(self.status['A3']),
            degToRad(self.status['A4']), degToRad(self.status['A5']), degToRad(self.status['A6'])]
        self.status['joints'] = chk.getJointCoordinates(a)

        #print(f'status: {self.status}')
        return self.status

    def connectSerial(self, port='/dev/ttyACM0'):
        # Serial port
        try:
            self.ser = serial.Serial(port, baudrate=9600)
            if self.ser.isOpen():
                self.ser.close()
            self.ser.open()
            log(f'Serial is opened at {port}', 0)
            self.status['serial'] = True
        except:
            log(f'Failed to open serial port at {port}', 0)
            self.status['serial'] = False

    def pushCommand(self, cmd):
        self.cmdQueue.append(cmd)

    def decExeCommand(self, cmd):
        cmd = cmd.split(';')[0].strip('\n')
        log(f'Command Received: {cmd}')
        paramtrs = cmd.split(' ')
        if (len(paramtrs) == 0):
            return
        
        # G0 - Move to stepper angle
        if (paramtrs[0] == 'G0'):
            for p in paramtrs:
                if (p[0] == 'A'):
                    instr = p[0:2]
                    op = float(p[2::])
                    self.status[instr] = op
                else:
                    op = float(p[1::])
                    self.status[p[0]] = op

            self.G0( self.status['A1'], self.status['A2'], self.status['A3'],
                self.status['A4'], self.status['A5'], self.status['A6'],
                self.status['F'] )

            # Update position as well
            a = [0, self.status['A1'], self.status['A2'], self.status['A3'],
                    self.status['A4'], self.status['A5'], self.status['A6']]
            X, Y, Z = chk.getJointCoordinates(a)[3]
            self.status['X'], self.status['Y'], self.status['Z'] = X, Y, Z
            
        # G1 - Move to position/rotation
        elif (paramtrs[0] == 'G1'):
            for p in paramtrs:
                op = float(p[1::])
                self.status[p[0]] = op
            
            self.G1( self.status['X'], self.status['Y'], self.status['Z'],
                self.status['P'], self.status['E'], self.status['R'],
                self.status['F'] )

            # Update angles as well
            a = ik.getAngles( self.status['X'], self.status['Y'], self.status['Z'],
                degToRad(self.status['P']), degToRad(self.status['E']), degToRad(self.status['R']))

            self.status['A1'], self.status['A2'] = radToDeg(a[0]), radToDeg(a[1])
            self.status['A3'], self.status['A4'] = radToDeg(a[2]), radToDeg(a[3])
            self.status['A5'], self.status['A6'] = radToDeg(a[4]), radToDeg(a[5])
        
        # G10 - Reset all steppers to zero
        elif (paramtrs[0] == 'G10'):
            self.G0(0, 0, 0, 0, 0, 0, 3)
            self.status['A1'], self.status['A2'] = 0, 0
            self.status['A3'], self.status['A4'] = 0, 0
            self.status['A5'], self.status['A6'] = 0, 0

            self.status['X'], self.status['Y'], self.status['Z'] = 0, 0, cf.L1+cf.L2+cf.L3+cf.L4
            self.status['P'], self.status['E'], self.status['R'] = 0, 90, 0

        # M0 - Serial Connect
        elif (paramtrs[0] == 'M0'):
            if (len(paramtrs) > 1):
                self.M0(paramtrs[1])
            else:
                self.M0()

        # M1 - Set Acceleration
        elif (paramtrs[0] == 'M1'):
            if self.status['serial'] and len(paramtrs) > 1:
                self.ser.write(bytes(f'A {float(paramtrs[1])}\n'.encode()))
            

    def readFile(self, path):
        path = os.path.abspath(path)
        log(f'>> Running script at {path}...', 0)
        script = open(path, 'r')
        lines = script.readlines()
        log('________STARTING________', 0)
        for line in lines:
            self.decExeCommand(line)
            time.sleep(2)
        log('________FINISHED________\n', 0)

    def moveMotors(self, a, F):
        if self.status['serial']:
            a_deg = [0, radToDeg(a[1]), radToDeg(a[2]), radToDeg(a[3]),
                        radToDeg(a[4]), radToDeg(a[5]), radToDeg(a[6])]
            serialCmd = f'M {a_deg[1]} {a_deg[2]} {a_deg[3]} {a_deg[4]} {a_deg[5]} {a_deg[6]} {F}\n'
            print(f'serialCmd: {serialCmd}')
            self.ser.write(bytes(serialCmd.encode()))


    def run(self):
        while True:
            if (len(self.cmdQueue) > 0):
                cmd = self.cmdQueue.pop(0)
                self.decExeCommand(cmd)


    #-------------------------------------------------------------
    #       LGCODE COMMANDS
    #-------------------------------------------------------------
    def G0(self, a1, a2, a3, a4, a5, a6, F):
        a_deg = [a1, a2, a3, a4, a5, a6]
        a = [0, degToRad(a1), degToRad(a2), degToRad(a3), degToRad(a4), degToRad(a5), degToRad(a6)]

        if (chk.checkAngleLimits(a)):
            printA(a_deg, '>> Angles: ')
            J6_x, J6_y, J6_z = chk.getJointCoordinates(a)[3]
            printA([J6_x, J6_y, J6_z], '>> Toolhead: ')

            self.moveMotors(a, F)
            time.sleep(F)
            # visualize.show(a)
        else:
            log('>> Error: Angles out of range.')

    def G1(self, Tx, Ty, Tz, Tap, Tae, Tar, F):
        Tap, Tae, Tar = degToRad(Tap), degToRad(Tae), degToRad(Tar) # convert to radian
        a1, a2, a3, a4, a5, a6 = ik.getAngles(Tx, Ty, Tz, Tap, Tae, Tar)
        if (a1 != -1):
            self.G0( radToDeg(a1), radToDeg(a2), radToDeg(a3),
                radToDeg(a4), radToDeg(a5), radToDeg(a6), F)

    def M0(self, port='/dev/ttyACM0'):
        self.connectSerial(port)