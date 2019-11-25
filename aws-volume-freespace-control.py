#!/usr/bin/python

import subprocess
import psutil
import time
import logging
import requests
import json
from systemd.journal import JournalHandler

log = logging.getLogger('demo')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

freeSpaceLowerLimit = 2                 # Freespace lower limit (in GB)
growupStep = 2                          # Partition grow up step (in GB)
checkInterval = 6                       # Check interval (in minutes)
EC2volumeId = "vol-0b748cdfc3f2658b3"   # EC2 volume ID
rootDrive = "/dev/xvda"                 # Name of root drive
rootPart = "/dev/xvda1"                 # Name of root partition
rootPartNum = "1"                       # Number of root partition
slackWebhook = "https://hooks.slack.com/services/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"

def getFreeSpace():
    diskUsage = psutil.disk_usage('/')
    diskFreeSpace = diskUsage.free / (1024 ** 3)
    log.info('Current free space: ' + str(diskFreeSpace))
    return diskFreeSpace

def checkFreeSpaceLimit(freeSpace):
    if freeSpace < freeSpaceLowerLimit:
        log.info('Need to growup!')
        return True
    else:
        log.info('All done!')
        return False

def getEC2VolumeSize():
    cmd = "aws ec2 describe-volumes --volume-ids=" + EC2volumeId + " | jq -r '.Volumes' | jq -r '.[].Size'"
    awsCurrentVolumeSizeRun = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    size, error = awsCurrentVolumeSizeRun.communicate()

    if error == '':
        log.info('Current volume size is: ' + str(size))
        return size
    else:
        log.info(error)
        return 0

def updateEC2VolumeSize(volumeSize):
    log.info('Trying to update EC2 volume size')
    cmd = "aws ec2 modify-volume --volume-id " + EC2volumeId + " --size " + str(volumeSize)
    awsUpdateVolumeSizeRun = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    size, error = awsUpdateVolumeSizeRun.communicate()

    if error == '':
        log.info('Please wait 120 sec')
        time.sleep(120)
        log.info('Update EC2 volume size is complete, new volume size is: ' + getEC2VolumeSize())
        time.sleep(120)
        return True
    else:
        log.info(error)
        return False

def updatePartitionSize():
    cmd = "growpart " + rootDrive + " " + rootPartNum
    updatePartitionSizeRun = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    size, error = updatePartitionSizeRun.communicate()

    if error == '':
        log.info('Update partition size is complete')
        return True
    else:
        log.info(error)
        return False
    
def resizeFs():
    cmd = "resize2fs " + rootPart
    resizeFsRun = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    size, error = resizeFsRun.communicate()

    if error == '':
        log.info('Resize FS is complete')
        return True
    else:
        log.info(error)
        return False

def sendSlackNotification():
    log.info('Send Slack notification')
    payload = {'text': "Free space warning!"}
    res = requests.post(slackWebhook, json=payload)

    if res.status_code != 200:
        log.info('Notification error... code: ' + str(res.status_code) + ' with content: ' + res.content)

def main():
    while True:
        freeSpace = getFreeSpace()
        if checkFreeSpaceLimit(freeSpace) == True:
	    sendSlackNotification()
            currentVolumeSize = getEC2VolumeSize()
            if currentVolumeSize != 0:
                newVolumeSize = int(currentVolumeSize) + growupStep
                if updateEC2VolumeSize(newVolumeSize) == True:
                    if updatePartitionSize() == True:
                        resizeFs()
        time.sleep(checkInterval * 100)

if __name__ == "__main__":
    main()
