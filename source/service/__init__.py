from kivy.utils import platform
from debug import Debug

class MonitorLaucher():
    monitor = None
    service = None
    
    def __init__(self, parameter=""):        
        Debug().log("Inicializando monitor")
        
        if platform == "android":
            import android
            try:
                self.service = android.AndroidService('SigmaWeb+', 'Monitorando') 
                self.service.start()
            except:
                raise MonitorException("Unable to create monitor service")
        else:
            import threading
            from main import Monitor 
            
            try:
                self.monitor = Monitor()
                
                self.service = threading.Thread(target=self.monitor.run)
                self.service.daemon = True
                self.service.name = "Monitor"
                self.service.start()
            except:
                raise MonitorException("Unable to create monitor thread")
            
    def kill(self, force=False):
        if (platform <> "android"):
            try:
                self.monitor.kill()
                self.service.join()
            except:
                raise MonitorException("Unable to kill thread")
        elif (force==True):
            try:
                self.service.stop()
            except:
                raise MonitorException("Unable to kill service")

class MonitorException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)