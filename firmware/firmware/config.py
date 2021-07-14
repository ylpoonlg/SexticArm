DEBUG_LOG_LEVEL = 1

#------------------------------------------
#   INPUT FILE
#------------------------------------------
SCRIPT_FOLDER_PATH = '../scripts/'

#------------------------------------------
#   MACHINE SETTINGS
#------------------------------------------
# Link lengths (in mm)
L1 = 150
L2 = 100
L3 = 100
L4 = 50

# Feedrate
DEFAULT_FEEDRATE = 2                            # (in mm/s)

# Angle limits
# (min, max)
ANGLES_LIMIT = [ (-1, -1), # dummy
    (0, 360),
    (270, 90),
    (270, 90),
    (0, 360),
    (270, 90),
    (0, 360)
]       # (in deg)