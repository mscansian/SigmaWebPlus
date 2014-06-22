from Singleton import Singleton

class Debug():    
    #Singleton
    __metaclass__ = Singleton
    
    HEADER   = '\033[95m'
    OKBLUE   = '\033[94m'
    OKGREEN  = '\033[92m'
    WARNING  = '\033[93m'
    FAIL     = '\033[91m'
    ENDC     = '\033[0m'
    
    #Configuration
    enabled = False
    
    def note(self, message, header="SigmaWeb"):
        if self.enabled: print self.OKGREEN + header + ": " + message + self.ENDC
    
    def warn(self, message, header="SigmaWeb"):
        if self.enabled: print self.WARNING + header + ": " + message + self.ENDC
        
    def error(self, message, header="SigmaWeb"):
        if self.enabled: print self.FAIL + header + ": " + message + self.ENDC