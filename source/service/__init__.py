from kivy.utils import platform
from debug import Debug

class ServiceLaucher():
    service = None
    thread = None
    
    def __init__(self, parameter=""):        
        Debug().log("Inicializando monitor")
        
        if platform == "android":
            import android
            try:
                self.service = android.AndroidService('SigmaWeb+', 'Monitorando') 
                self.service.start()
            except:
                raise ServiceException("Unable to create monitor service")
        else:
            import threading
            from main import Service 
            
            try:
                self.service = Service()
                
                self.thread = threading.Thread(target=self.service.run)
                self.thread.daemon = True
                self.thread.name = "Service"
                self.thread.start()
            except:
                raise ServiceException("Unable to create service thread")
            
    def kill(self, force=False):
        if (platform <> "android"):
            try:
                self.service.kill()
                self.thread.join()
            except:
                raise ServiceException("Unable to kill thread")
        elif (force==True):
            try:
                self.service.stop()
            except:
                raise ServiceException("Unable to kill service")

class ServiceException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)