#!/usr/bin/python
import time
import yaml

from procWatcher import procWatcher
from volumeWatcher import volumeWatcher

def main():
    procThread = procWatcher.WatcherThread(config["proc"])
    procThread.start()

    volumeThread = volumeWatcher.WatcherThread(config["volume"])
    volumeThread.start()



if __name__ == "__main__":
    with open("./centry-config.yml", "r") as configFile:
        config = yaml.load(configFile, Loader=yaml.FullLoader)
    main()
