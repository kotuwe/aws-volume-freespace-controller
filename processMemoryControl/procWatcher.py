import time
import threading
import psutil
import subprocess
import logging
from systemd.journal import JournaldLogHandler

log = logging.getLogger('centry')
log.addHandler(JournaldLogHandler())
log.setLevel(logging.INFO)

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
        self.interval = config["checkInterval"]
    
    def run(self):
        self.checkEnabled = True
        while(self._running):
            log.info('Check process memory for: ' + self.procName)
            self.checkProc(self.procName, self.startLine)
            time.sleep(self.interval)

    def stop(self):
        self._running = False

    def checkProc(self, procName, startLine):
        totalMemory = 0
        totalProc = 0
        for proc in psutil.process_iter():
            try:
                if procName.lower() in proc.name().lower():
                    rss = proc.memory_info().rss / 1024 / 1024 / 1024
                    totalMemory += rss
                    totalProc += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        log.info("Total memory used by process: " + str(totalMemory))
        log.info("Total process count: " + str(totalProc))
        if totalMemory > self.memoryLimit:
            log.info("Try to restart process")
            for proc in psutil.process_iter():
                try:
                    if procName.lower() in proc.name().lower():
                        try:
                            proc.kill()
                        except psutil.NoSuchProcess:
                            pass                
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            subprocess.Popen(startLine, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)