from kivy.utils import platform
from debug import Debug

class MonitorLaucher():
    _platform = None
    _monitor = None
    _thread = None
    _service = None
    
    def __init__(self, parameter=""):
        self._platform = platform
        
        Debug().log("Inicializando monitor")
        
        if platform == "android":
            import android
            try:
                self._service = android.AndroidService('SigmaWeb+', 'Monitorando') 
                self._service.start()
            except:
                raise MonitorException("Unable to create monitor service")
        else:
            import threading
            from main import Monitor 
            
            try:
                self._monitor = Monitor()
                
                self._thread = threading.Thread(target=self._monitor.run)
                self._thread.daemon = True
                self._thread.name = "Monitor"
                self._thread.start()
            except:
                raise MonitorException("Unable to create monitor thread")
            
    def kill(self, force=False):
        if (platform <> "android"):
            try:
                self._monitor.kill()
                self._thread.join()
                print 'fim'
            except:
                raise MonitorException("Unable to kill thread")
        elif (force==True):
            try:
                self._service.stop()
            except:
                raise MonitorException("Unable to kill service")

class MonitorException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)