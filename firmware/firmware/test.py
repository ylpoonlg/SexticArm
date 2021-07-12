import firmware as fw

machine = fw.lgcode.lgcodeReader()

def getTestPoints():
    points = []
    count = 0

    maxZ = fw.config.L1 + fw.config.L2 + fw.config.L3 + fw.config.L4
    for i in range(-200, 201, 10):
        for j in range(-200, 201, 10):
            for k in range(0, maxZ+1, 10):
                Tap, Tae, Tar = 0, 0, 0
                a = fw.ik.getAngles(i, j, k, Tap, Tae, Tar)

                print(f'[{count}] Testing ({i}, {j}, {k}) | ({Tap}, {Tae}, {Tar})')
                count += 1

                if (a[0] != -1):
                    points.append(([i, j, k], True))
                else:
                    points.append(([i, j, k], False))

    return points                    


if __name__ == '__main__':
    points = getTestPoints()
    print(f'testPoints = {points}')