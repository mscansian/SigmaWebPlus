#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time, http, random

from kivy.utils import platform
from notification_demo.components.notification import Notification
from threadcomm.threadcomm import ThreadComm, ThreadCommServer


class Service():
    #Objects
    threadComm = None
    sigmaWeb = None
    
    #Signals
    _SIGTERM = False
    
    #Configuration
    verifyTimeout = None #Seconds
    verifyAuto = False
    lastCheck = 0
    
    def run(self):
        print "Monitor: Started successfully"
        
        #Start ThreadComm
        self.threadComm = ThreadComm(51352, "sigmawebplus", ThreadCommServer)
        self.threadComm.start()
        
        #Start SigmaWebMonitor
        self.sigmaWeb = SigmaWebMonitor()
        
        #Run until SIGTERM
        while (self._SIGTERM==False):
            #Listen and respond to ThreadComm messages
            self.listen()
            
            #Verifica por novas notas no sistema
            if self.verifyAuto and self.sigmaWeb.enoughInfo(): #Checka se o monitor esta autorizado a verificar notas e o SigmaWebMonitor tem informacoes suficientes
                if (self.lastCheck + self.verifyTimeout) < time.time():                    
                    try:
                        print "Debug: Fetching data from server..."
                        notification, response = self.sigmaWeb.check()
                    except SigmaWebMonitorException as e:
                        if str(e)[1:15] == "Server error: ":
                            self.threadComm.sendMsg("ERR "+str(e)[15:-1])
                        elif str(e)  == "'Data is already up to date'":
                            self.threadComm.sendMsg("UTD ")
                        elif str(e) == "'Unable to fetch data from server'":
                            print "Monitor: Unable to fetch data from server"
                        else:
                            raise
                    else:
                        self.threadComm.sendMsg("NNA "+response)
                        
                        if notification:
                            Notification("SigmaWeb+","Novas notas disponiveis!").notify()
                    self.lastCheck = time.time()
            
            time.sleep(1)
        
        self.threadComm.sendMsg("CLS")
        self.threadComm.stop()
        print "Monitor: Killed successfully"
    
    def kill(self):
        self._SIGTERM = True
    
    def listen(self):
        #Check for ThreadComm messages
        try:
            message = self.threadComm.recvMsg()
        except:
            return False
        
        print message
        if message[:3] == "TOC": #Timeout change
            self.verifyTimeout = float(message[4:]) * 60
        elif message[:3] == "ATC": #Auto check
            self.verifyAuto = (message[4:] == "1")
        elif message[:3] == "CKN": #Check now
            self.lastCheck = 0
        elif message[:3] == "KIL": #Kill
            self.threadComm.sendMsg("SH1 "+str(self.lastCheck))
            self.threadComm.sendMsg("SH2 "+self.sigmaWeb.getData())
            self._SIGTERM = True
        elif message[:3] == "SNT": #Send notification
            Notification("SigmaWeb+",message[4:]).notify()
        elif message[:3] == "UNC": #Username change
            self.sigmaWeb.setUsername(message[4:])
            self.lastCheck = 0  
        elif message[:3] == "UNP": #Password change
            self.sigmaWeb.setPassword(message[4:])
            self.lastCheck = 0
        elif message[:3] == "HSC": #Hash change
            self.sigmaWeb.setHash(message[4:])
            self.lastCheck = 0
        elif message[:3] == "LCK": #Hash change
            self.lastCheck = float(message[4:])
            print self.lastCheck
            print time.time()
        return True
        
class SigmaWebMonitor:
    username = None
    password = None
    hash = None
    data = None
    
    def check(self):
        if not self.enoughInfo():
            raise SigmaWebMonitorException("Not enough data to fetch information from server")
        
        try:
            pagina = http.Page("http://www.sigmawebplus.com.br/server/")
            pagina.set_RequestHeaders(http.Header("username", self.username), http.Header("password", self.password), http.Header("hash", self.hash))
            pagina.Refresh()
            response = pagina.get_ResponseData()
        except:
            raise SigmaWebMonitorException("Unable to fetch data from server")
        
        #Avalia a resposta
        if response[:7] == "<error>":
            raise SigmaWebMonitorException("Server error: "+response[7:-8])
        elif response[:10] == "Up-to-date":
            raise SigmaWebMonitorException("Data is already up to date")
        
        notification = not (self.hash == "")
        self.hash = response[:32]
        self.data = response
        return notification, response
    
    def enoughInfo(self):
        if (self.username == None) or (self.password==None) or (self.hash==None):
            return False
        else:
            return True
            
    
    def setUsername(self, username):
        if not (username == ""):
            self.username = username
    
    def setPassword(self, password):
        if not (password==""):
            self.password = password
    
    def setHash(self, hash):
        self.hash = hash
        
    def getData(self):
        if not (self.data == None):
            return self.data
        return ""
        
class SigmaWebMonitorException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)            
        

if __name__ == '__main__':
    #On Android platform this code is executed automaticaly
    Service().run()