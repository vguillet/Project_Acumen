import numpy as np
import numpy.random as random

def randomstats(file, r):

    f = open(file, 'a')

    xdat = np.arange(0, r)
    ydat = np.random.randint(0, 10, r)

    for i in range(r):
        f.write('{0},{1}\n'.format(xdat[i], ydat[i]))

    f.close()

    return

randomstats('testdata1.txt', 200)
randomstats('testdata2.txt', 200)
randomstats('testdata3.txt', 200)