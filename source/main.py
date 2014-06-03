#!/usr/bin/python
# -*- coding: UTF-8 -*-

from kivy.utils import platform
from kivyapp import KivyApp

class SigmaWeb:
    _singleinstance = None
    _kivy = None
    _ThreadComm = None
    _Service = None
    
    def __init__(self):
        pass

    def run(self):
        self.on_Start()
    
    def on_Start(self):
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
        self._kivy = KivyApp()
        self._kivy.setCallbacks(self.update, self.on_ConfigChanged, self.on_Exit, self.on_NotasRequested)
        self._kivy.run()
        
    
    def on_Exit(self):
        self._singleinstance.kill()
        self._ThreadComm.kill()
        self._Service.kill()
    
    def update(self, *args):
        message = self._ThreadComm.recvMsg()
        if message <> None:
            if message[:3] == "NNA": #New Notas Available
                self._kivy.updateNotas(message[4:])
            elif message[:3] == "UPW": #Usuario ou matricula errado
                pass
        
    
    def on_ConfigChanged(self, config, value):
            if config == 'timeout':
                self._ThreadComm.sendMsg("TOC "+value)
            elif config == 'login':
                self._ThreadComm.sendMsg("UNC "+value)
            elif config == 'password':
                self._ThreadComm.sendMsg("UNP "+value)
            elif config == 'hash':
                self._ThreadComm.sendMsg("HSC "+value)
            elif config == 'auto_timeout':
                self._ThreadComm.sendMsg("ATC "+value)
                    
    def on_NotasRequested(self):
        self._ThreadComm.sendMsg("CKN")

if __name__ == '__main__':
    SigmaWeb().run()