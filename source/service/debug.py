from Singleton import Singleton

class Debug():
    #Use singleton for the event handler
    __metaclass__ = Singleton
    
    def log(self, message):
        print "SIGMAWEB: "+message