import firmware as fw

machine = fw.lgcode.lgcodeReader()

def getTestPoints(sep=20):
    points = []
    count = 0

    maxZ = fw.config.L1 + fw.config.L2 + fw.config.L3 + fw.config.L4
    maxXY = maxZ - fw.config.L1
    for i in range(-maxXY, maxXY+1, sep):
        for j in range(-maxXY, maxXY+1, sep):
            for k in range(0, maxZ+1, sep):
                Tap, Tae, Tar = 0, 90, 0
                a = fw.ik.getAngles(i, j, k, Tap, Tae, Tar)

                print(f'[{count}] Testing ({i}, {j}, {k}) | ({Tap}, {Tae}, {Tar})')
                count += 1

                if (a[0] != -1):
                    points.append(([i, j, k], True))
                else:
                    points.append(([i, j, k], False))

    return points                    


if __name__ == '__main__':
    points = getTestPoints(sep=50)
    print(f'testPoints = {points}')