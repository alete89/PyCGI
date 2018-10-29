#!/usr/bin/python

import sys
import time

print 'Number of arguments:', len(sys.argv), 'arguments.'
for argumento in sys.argv:
    print str(argumento)
    time.sleep(3)
