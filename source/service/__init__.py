from kivy.utils import platform

class ServiceLaucher():
    service = None
    thread = None
    
    def __init__(self):
        if platform == "android":
            import android
            self.service = android.AndroidService('SigmaWeb+', 'Monitorando')
    
    def start(self):        
        
        if platform == "android":
            self.service.start()
        else:
            import threading
            from main import Service 
            
            self.service = Service()    
            self.thread = threading.Thread(target=self.service.run)
            self.thread.daemon = False
            self.thread.name = "Service"
            self.thread.start()
            
    def kill(self):
        if platform == "android":
            self.service.stop()
        else:
            self.service.kill()
            self.thread.join()