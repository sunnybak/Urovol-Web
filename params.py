def getParams():
    f = open("params.txt", 'r')
    p = [x.split('=')[1] for x in f.read().split('\n') if len(x) > 0]
    p = (int(p[0]), int(p[1]), int(p[2]), int(p[3]), int(p[4]), float(p[5]), int(p[6]))
    f.close()
    print("Get params")
    return p

def setParams(p):
    f = open("params.txt", 'w')
    s = 'AVG=' + str(p[0]) + '\n' + \
        'STD=' + str(p[1]) + '\n' + \
        'LASTN=' + str(p[2]) + '\n' + \
        'DIFF_MIN=' + str(p[3]) + '\n' + \
        'DIFF_MAX=' + str(p[4]) + '\n' + \
        'MULT=' + str(p[5]) + '\n' + \
        'INTV=' + str(p[6]) + '\n'
    f.write(s)
    f.close()
    print("Set params")

# setParams((1432, 14, 6, 10, 000, 0.93, 3300))
# print(getParams())