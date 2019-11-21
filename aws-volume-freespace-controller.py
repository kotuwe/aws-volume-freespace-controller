#!/usr/bin/python

import subprocess
import psutil

freeSpaceLowerLimit = 7000

def getFreeSpace():
    diskUsage = psutil.disk_usage('/')
    diskFreeSpace = diskUsage.free / (1024 ** 2)
    print('Current free space: ', diskFreeSpace)
    return diskFreeSpace

def checkFreeSpaceLimit():
    if getFreeSpace() < freeSpaceLowerLimit:
        print('Need to growup!')
    else:
        print('All done!')

checkFreeSpaceLimit()
