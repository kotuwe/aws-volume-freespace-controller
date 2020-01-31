#!/usr/bin/python3
import time
import yaml

import processMemoryControl.procWatcher as procWatcher
import volumeFreespaceControl.volumeWatcher as volumeWatcher

def main():
    processThread = procWatcher.WatcherThread(self.config["processMemoryControl"])
    processThread.start()

    volumeThread = volumeWatcher.WatcherThread(self.config["volumeFreespaceControl"])
    volumeThread.start()



if __name__ == "__main__":
    with open("/etc/centry.yml", "r") as configFile:
        self.config = yaml.load(configFile, Loader=yaml.FullLoader)
    main()
