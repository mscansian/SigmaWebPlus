#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
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
    enabled = True
    
    def note(self, message, header="SigmaWeb"):
        if self.enabled: print self.OKGREEN + header + ": " + message + self.ENDC
    
    def warn(self, message, header="SigmaWeb"):
        if self.enabled: print self.WARNING + header + ": " + message + self.ENDC
        
    def error(self, message, header="SigmaWeb"):
        if self.enabled: print self.FAIL + header + ": " + message + self.ENDC