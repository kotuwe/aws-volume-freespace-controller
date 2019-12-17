#!/usr/bin/python

import subprocess
import psutil
import time
import logging
import requests
import json
from systemd.journal import JournaldLogHandler

from procWatcher import procWatcher
from volumeWatcher import volumeWatcher

def main():
    procThread = procWatcher.WatcherThread('smth')
    procThread.start()
    time.sleep(3)
    print('stop proc watcher thread')
    procThread.stop()

    volumeThread = volumeWatcher.WatcherThread()
    volumeThread.start()



if __name__ == "__main__":
    main()
