#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
from kivy.utils import platform
from kivyapp import KivyApp
from service import ServiceLaucher
from service.threadcomm.threadcomm import ThreadComm, ThreadCommException, ThreadCommClient
from singleinstance.singleinstance import SingleInstance 

class SigmaWeb:
    singleInstance = None
    kivy = None
    threadComm = None
    service = None
    
    def __init__(self):
        pass

    def run(self):
        self.on_start()
    
    def on_start(self):
        #Creates a handle for SingleInstance (this is not necessary on Android 'cause the OS takes care of this!
        if platform <> 'android':
            self.singleInstance = SingleInstance(50363, False)
        
        #Load ThreadComm and check if service is running
        dadoNotas = None
        self.threadComm = ThreadComm(51352, "sigmawebplus", ThreadCommClient)
        try:
            self.threadComm.start()
        except ThreadCommException:
            pass #Service is not running, keep going
        else:
            #Service is running. Get all info from server and ask to shutdown
            self.threadComm.sendMsg("KIL")
            while True:
                try:
                    message = self.threadComm.recvMsg()
                except ThreadCommException:
                    pass
                else:
                    if message[:3] == "SH2":
                        dadoNotas = dadoNotas + [message[4:(32+4)], message[(32+5):]]
                    elif message[:3] == "SH1":
                        dadoNotas = [message[4:]]
                    elif message == "CLS":
                        break
        
        #Load Service
        self.service = ServiceLaucher()
        
        #Connect Threadcomm
        Connected = False
        while not Connected:
            try:
                self.threadComm.start()
            except ThreadCommException:
                pass
            else:
                Connected = True
        
        #Load and start kivy
        self.kivy = KivyApp()
        self.kivy.setCallback(self.update, self.on_event)
        self.kivy.nextUpdate = dadoNotas
        self.kivy.run()
        
    
    def on_stop(self):
        if platform <> 'android':
            self.singleInstance.kill()
        self.threadComm.stop()
        #self.service.kill(force=True)
    
    def update(self, *args):
        try:
            message = self.threadComm.recvMsg()
        except ThreadCommException as e:
            pass
        else:
            if message[:3] == "NNA": #New Notas Available
                #Separa notas e Hash
                hash = message[4:(32+4)]
                notas = message[(32+5):]
                
                #Manda as notas para a aplicacao kivy
                self.kivy.updateNotas(hash, notas, 'Novas notas disponiveis!\n\nAtualizado em: '+time.strftime("%x %X")+'\n\n\nDeslize para visualizar')
            elif message[:3] == "UTD":
                self.kivy.updateNotas('', '', '\n\nAtualizado em: '+time.strftime("%x %X")+'\n\n\nDeslize para visualizar')
            elif message[:3] == "ERR": #Erro no servidor
                if message[4:] == "Auth error":
                    self.kivy.on_event("Logoff") #Log user off
        
    def on_event(self, eventType, *args):
        if eventType == "VerificarNotas":
            self.threadComm.sendMsg("CKN")
        elif eventType == "ConfigChange":
            config = args[2]
            value = args[3]
            if config == 'update_time':
                self.threadComm.sendMsg("TOC "+value)
            elif config == 'update_auto':
                self.threadComm.sendMsg("ATC "+value)
            else:
                pass
        elif eventType == "Login":
            self.threadComm.sendMsg("UNC "+args[0])
            self.threadComm.sendMsg("UNP "+args[1])
        elif eventType == "Logoff":
            self.threadComm.sendMsg("UNC ")
            self.threadComm.sendMsg("UNP ")
        elif eventType == "ProgramStart":
            self.threadComm.sendMsg("LCK "+args[0])
            self.threadComm.sendMsg("HSC "+args[1])
            self.threadComm.sendMsg("TOC "+args[2])
            self.threadComm.sendMsg("ATC "+args[3])
        elif eventType == "ProgramExit":
            self.on_stop()
        else:
            print "Warning: Event caught but not recognized '"+eventType+"' in main.py"

if __name__ == '__main__':
    SigmaWeb().run()