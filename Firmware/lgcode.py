import numpy as np
import os
import config as cf

class lgcodeRead():
    def __init__(self, script_path):
        super().__init__()
        path = os.path.abspath(script_path)
        print(f'path = {path}')
        self.script = open(path, 'r')

    def readlns(self):
        # Store current states
        X = 0
        Y = 0
        Z = 0
        P = 0
        E = 0
        R = 0
        F = 200

        lines = self.script.readlines()
        result = []
        for line in lines:
            cmds = line.split(' ')
            if (len(cmds) == 0):
                continue
            if cmds[0] == 'G0':
                for cmd in cmds:
                    cmd = cmd.strip("\n")
                    if (cmd[0] == 'X'):
                        X = float(cmd[1::])
                    elif (cmd[0] == 'Y'):
                        Y = float(cmd[1::])
                    elif (cmd[0] == 'Z'):
                        Z = float(cmd[1::])
                    elif (cmd[0] == 'P'):
                        P = float(cmd[1::])
                    elif (cmd[0] == 'E'):
                        E = float(cmd[1::])
                    elif (cmd[0] == 'R'):
                        R = float(cmd[1::])
                    elif (cmd[0] == 'F'):
                        F = float(cmd[1::])
                result.append({ 'cmd': 'G0',
                    'X': X, 'Y': Y, 'Z': Z,
                    'P': P, 'E': E, 'R': R,
                    'F': F
                })


        return result
        