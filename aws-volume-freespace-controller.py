#!/usr/bin/python

import subprocess
import psutil

freeSpaceLowerLimit = 7
growupStep = 2
EC2volumeId = "vol-0b748cdfc3f2658b3"

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

def getEC2VolumeSize():
    cmd = "aws ec2 describe-volumes --volume-ids=" + EC2volumeId + " | jq -r '.Volumes' | jq -r '.[].Size'"
    awsCurrentVolumeSize = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    size, error = awsCurrentVolumeSize.communicate()

    if error == '':
        print('Current volume size is: ' + str(size) + 'GB')
        return size
    else:
        return 0

def updateEC2VolumeSize(volumeSize):
    cmd = "aws ec2 modify-volume --volume-id " + EC2volumeId + " --size " + str(volumeSize)
    awsUpdateVolumeSize = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    size, error = awsUpdateVolumeSize.communicate()

    if error == '':
        print('Update is complete, new volume size is: ' + getEC2VolumeSize())
        return True
    else:
        return False
    

freeSpace = getFreeSpace()
if checkFreeSpaceLimit(freeSpace) == True:
    currentVolumeSize = getEC2VolumeSize()
    if currentVolumeSize != 0:
        newVolumeSize = int(currentVolumeSize) + growupStep
        updateEC2VolumeSize(newVolumeSize)
