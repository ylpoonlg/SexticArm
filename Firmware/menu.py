import os
import numpy as np
import config as cf
from lgcode import lgcodeReader
import lgcode
import visualize

class Menu():
    def __init__(self):
        self.page = 'home'
        self.isRunning = True
        while self.isRunning:
            print('________READY________')
            instr = input('Select Mode (h for help): ')
            if instr == 'h':
                print('''
Help
    q - quit
    f - run from file
    m - manual mode
                ''')
            elif instr == 'q':
                self.isRunning = False
            elif instr == 'f':
                self.fileMode()
            elif instr == 'm':
                self.manualMode()
            else:
                print('>> Invalid command')

    def getFilePath(self):
        print(f'Scanning files in {cf.SCRIPT_FOLDER_PATH}...')
        files = os.listdir(cf.SCRIPT_FOLDER_PATH)
        for i in range(len(files)):
            print(f' - {i}: {files[i]}')
        select_file = input(f'Select a file (0-{len(files)-1}; default=0)(h for help): ')

        if (select_file == 'q' or select_file == 'b' or select_file == 'h'):
            return select_file
        
        try:
            script_file_name = files[0]
            if (select_file != ''):
                script_file_name = files[int(select_file)]

            if (cf.SCRIPT_FOLDER_PATH[-1] != '/'):
                script_file_name = '/' + script_file_name
            
            return cf.SCRIPT_FOLDER_PATH+script_file_name
        except:
            print('Input Invalid...')

        return '-1'
    
    def fileMode(self):
        print('\n[File Mode]')
        while True:

            path = self.getFilePath()
            if path == 'q':
                self.isRunning = False
                break
            elif path == 'b':
                break
            elif path == 'h':
                print('''
Help
    0,1,2,3,... - select file you want to run
    q - quit
    b - back to home page
                ''')
                continue

            visualize.init() # New display window
            reader = lgcodeReader()
            reader.readFile(path)

    def manualMode(self):
        visualize.init() # New display window
        print('\n[Manual Mode]')
        reader = lgcodeReader()
        while True:
            cmd = input('Enter Command (h for help): ')
            if cmd == 'q':
                self.isRunning = False
                break
            elif cmd == 'b':
                break
            elif cmd == 'h':
                print('''
Help
    Please refer to the documentation for list of LGCODE commands:
        https://github.com/ylpoonlg/6DOF
    q - quit
    b - back to home page
                ''')
                continue

            reader.decExeCommand(cmd)