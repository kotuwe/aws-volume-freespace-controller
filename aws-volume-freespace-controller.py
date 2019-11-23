#!/usr/bin/python

import subprocess
import psutil
import time

freeSpaceLowerLimit = 7
growupStep = 2
EC2volumeId = "vol-0b748cdfc3f2658b3"
rootDrive = "/dev/nvme0n1"
rootPart = "/dev/nvme0n1p1"
rootPartNum = "1"

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
    awsCurrentVolumeSizeRun = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    size, error = awsCurrentVolumeSizeRun.communicate()

    if error == '':
        print('Current volume size is: ' + str(size) + 'GB')
        return size
    else:
        return 0

def updateEC2VolumeSize(volumeSize):
    print('Trying to update EC2 volume size')

    cmd = "aws ec2 modify-volume --volume-id " + EC2volumeId + " --size " + str(volumeSize)
    awsUpdateVolumeSizeRun = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    size, error = awsUpdateVolumeSizeRun.communicate()

    if error == '':
        print('Please wait 120 sec')
        time.sleep(120)
        print('Update EC2 volume size is complete, new volume size is: ' + getEC2VolumeSize())
        time.sleep(120)
        return True
    else:
        return False

def updatePartitionSize():
    cmd = "growpart " + rootDrive + " " + rootPartNum
    updatePartitionSizeRun = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    size, error = updatePartitionSizeRun.communicate()

    if error == '':
        print('Update partition size is complete')
        return True
    else:
        return False
    
def resizeFs():
    cmd = "resize2fs " + rootPart
    resizeFsRun = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    size, error = resizeFsRun.communicate()

    if error == '':
        print('Resize FS is complete')
        return True
    else:
        return False

freeSpace = getFreeSpace()
if checkFreeSpaceLimit(freeSpace) == True:
    currentVolumeSize = getEC2VolumeSize()
    if currentVolumeSize != 0:
        newVolumeSize = int(currentVolumeSize) + growupStep
        if updateEC2VolumeSize(newVolumeSize) == True:
            if updatePartitionSize() == True:
                resizeFs()
