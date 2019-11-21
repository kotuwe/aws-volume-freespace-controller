#!/usr/bin/python

import subprocess
import psutil

def getFreeSpace():
    diskUsage = psutil.disk_usage('/')
    diskFreeSpace = diskUsage.free / (1024 ** 3)
    print('Current free space: ', diskFreeSpace)

getFreeSpace()
