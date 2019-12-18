import time
import threading
import psutil
import subprocess

class WatcherThread(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        if config["enable"] == True:
            self._running = True
        else:
            self._running = False
        self.procName = config["name"]
        self.memoryLimit = config["memoryLimit"]
        self.startLine = config["startLine"]
    
    def run(self):
        self.checkEnabled = True
        while(self._running):
            print('Check process memory for: ', self.procName)
            self.checkProc(self.procName, self.startLine)
            time.sleep(5)

    def stop(self):
        self._running = False

    def checkProc(self, procName, startLine):
        totalMemory = 0
        for proc in psutil.process_iter():
            try:
                if procName.lower() in proc.name().lower():
                    rss = proc.memory_info().rss / 1024 / 1024 / 1024
                    totalMemory += rss
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        print("Total memory used by process: ", totalMemory)
        if totalMemory > self.memoryLimit:
            print("Try to restart process")
            for proc in psutil.process_iter():
                try:
                    if procName.lower() in proc.name().lower():
                        proc.kill()
                
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            subprocess.Popen(startLine, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)