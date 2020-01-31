#!/usr/bin/python
import time
import yaml

from processMemoryControl import procWatcher
from volumeFreespaceControl import volumeWatcher

def main():
    procThread = procWatcher.WatcherThread(config["processMemoryControl"])
    procThread.start()

    volumeThread = volumeWatcher.WatcherThread(config["volumeFreespaceControl"])
    volumeThread.start()



if __name__ == "__main__":
    with open("/etc/centry.yml", "r") as configFile:
        config = yaml.load(configFile, Loader=yaml.FullLoader)
    main()
