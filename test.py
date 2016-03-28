from random import *
import os
add = open('add.csv', 'a')
sub = open('sub.csv', 'a')
mul = open('mul.csv', 'a')
div = open('div.csv', 'a')
c = 0
for t in xrange(1000):
    x = random() * 1000 - 500
    y = random() * 1000 - 500
    line = 0
    res = os.popen('python MyFloat.py ' + str(x) + ' ' + str(y) + ' 2> /dev/null').readlines()
    if len(res) == 4:
        add.write(res[0])
        sub.write(res[1])
        mul.write(res[2])
        div.write(res[3])
    else:
        print ('cur error %d' % c)
        c += 1
