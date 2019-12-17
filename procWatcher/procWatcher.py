import time
import threading

class WatcherThread(threading.Thread):
    def __init__(self, processName):
        threading.Thread.__init__(self)
        self.processName = processName
        self._running = True
    
    def run(self):
        self.checkEnabled = True
        while(self._running):
            print('Check process memory')
            time.sleep(5)

    def stop(self):
        self._running = False
