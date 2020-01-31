#!/usr/bin/python3
import time
import yaml

import processMemoryControl.procWatcher as procWatcher
import volumeFreespaceControl.volumeWatcher as volumeWatcher

def main():
    processThread = procWatcher.WatcherThread(config["processMemoryControl"])
    processThread.start()

    volumeThread = volumeWatcher.WatcherThread(config["volumeFreespaceControl"])
    volumeThread.start()



if __name__ == "__main__":
    with open("/etc/centry.yml", "r") as configFile:
        config = yaml.load(configFile, Loader=yaml.FullLoader)
    main()
