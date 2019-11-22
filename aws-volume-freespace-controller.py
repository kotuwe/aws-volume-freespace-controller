#!/usr/bin/python

import subprocess
import psutil

freeSpaceLowerLimit = 7

def getFreeSpace():
    diskUsage = psutil.disk_usage('/')
    diskFreeSpace = diskUsage.free / (1024 ** 3)
    print('Current free space: ' + str(diskFreeSpace))
    return diskFreeSpace

def checkFreeSpaceLimit(freeSpace):
    if freeSpace < freeSpaceLowerLimit:
        print('Need to growup!')
        return True
    else:
        print('All done!')
        return False

def growUpVolume(freeSpace):
    cmd = "aws ec2 describe-volumes --volume-ids=vol-0b748cdfc3f2658b3 | jq -r '.Volumes' | jq -r '.[].Size'"
    awsCurrentVolumeSize = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = awsCurrentVolumeSize.communicate()

    print(output)
    print(error)

freeSpace = getFreeSpace()
if checkFreeSpaceLimit(freeSpace) == True:
    growUpVolume(freeSpace)
