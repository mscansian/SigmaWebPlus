#!/usr/bin/python
# -*- coding: UTF-8 -*-

from kivy.utils import platform
from kivyapp import KivyApp

class SigmaWeb:
    _singleinstance = None
    kivy = None
    _ThreadComm = None
    _Service = None
    
    def __init__(self):
        pass

    def run(self):
        self.on_start()
    
    def on_start(self):
        #Creates a handle for SingleInstance (this is not necessary on Android 'cause the OS takes care of this!
        if platform <> 'android':
            try:
                from singleinstance import singleinstance
                self._singleinstance = singleinstance.SingleInstance(50362, False)
            except singleinstance.SingleInstanceException as e:
                raise
        
        #Load Threadcomm
        try:
            from service.threadcomm import threadcomm
            self._ThreadComm = threadcomm.ThreadComm(51352, "sigmawebplus")
            self._ThreadComm.waitReady()
        except threadcomm.ThreadCommException as e:
            raise
        
        #Load Service
        import service
        try:
            self._Service = service.ServiceLaucher()
            self._ThreadComm.waitConnected()
            print self._ThreadComm.mode
        except:
            raise #your hands
        
        #Load and start kivy
        self.kivy = KivyApp()
        self.kivy.setCallback(self.update, self.on_event)
        self.kivy.run()
        
    
    def on_stop(self):
        if platform <> 'android':
            self._singleinstance.kill()
        self._ThreadComm.kill()
        self._Service.kill(force=True)
    
    def update(self, *args):
        message = self._ThreadComm.recvMsg()
        if message <> None:
            if message[:3] == "NNA": #New Notas Available
                #Separa notas e Hash
                hash = message[4:(32+4)]
                notas = message[(32+5):]
                
                #Manda as notas para a aplicacao kivy
                self.kivy.updateNotas(hash, notas, 'Deslize para ver as notas')
            elif message[:3] == "ERR": #Erro no servidor
                print "*"+message[4:]+"*"
                if message[4:] == "Auth error":
                    self.kivy.on_event("Logoff") #Log user off
        
    def on_event(self, eventType, *args):
        if eventType == "VerificarNotas":
            self._ThreadComm.sendMsg("CKN")
        elif eventType == "ConfigChange":
            config = args[2]
            value = args[3]
            if config == 'timeout':
                self._ThreadComm.sendMsg("TOC "+value)
            elif config == 'auto_timeout':
                self._ThreadComm.sendMsg("ATC "+value)
            else:
                pass
        elif eventType == "Login":
            self._ThreadComm.sendMsg("UNC "+args[0])
            self._ThreadComm.sendMsg("UNP "+args[1])
        elif eventType == "Logoff":
            self._ThreadComm.sendMsg("UNC ")
            self._ThreadComm.sendMsg("UNP ")
        elif eventType == "ProgramStart":
            self._ThreadComm.sendMsg("HSC "+args[0])
            self._ThreadComm.sendMsg("TOC "+args[1])
            self._ThreadComm.sendMsg("ATC "+args[2])
        elif eventType == "ProgramExit":
            self.on_stop()
        else:
            print "Warning: Event caught but not recognized '"+eventType+"' in main.py"

if __name__ == '__main__':
    SigmaWeb().run()