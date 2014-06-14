#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time, http, random

from kivy.logger import Logger
from kivy.utils import platform
from notification_demo.components.notification import Notification


if platform <> "android":
    from service.debug import Debug
else:
    from debug import Debug

class Service():
    _exit = False
    
    _verifyTimeout = 0 #Minutes
    _verifyAuto = 0
    _username = ""
    _password = ""
    _lastHash = ""
    
    nome = None
    
    def run(self):
        self.nome = int(random.random()*100)
        Debug().log("Monitor: Started successfully")
        
        #Start ThreadComm
        try:
            from threadcomm import threadcomm
            ThreadComm = threadcomm.ThreadComm(51352, "sigmawebplus")
            ThreadComm.waitConnected()
        except threadcomm.ThreadCommException as e:
            sys.exit(e.value)
        
        #Run until SIGTERM
        lastCheck = 0
        while (self._exit==False):
            Debug().log("Service running... "+str(self.nome))
            
            #Check for ThreadComm messages
            message = ThreadComm.recvMsg()
            if message <> None:
                print "Service RCV: "+message
                if message[:3] == "TOC": #Timeout change
                    self._verifyTimeout = float(message[4:])
                elif message[:3] == "ATC": #Auto check
                    self._verifyAuto = message[4:]
                elif message[:3] == "CKN": #Check now
                    lastCheck = 0
                elif message[:3] == "KIL": #Kill
                    self._exit = True
                elif message[:3] == "SNT": #Send notification
                    Notification("SigmaWeb+",message[4:]).notify()
                elif message[:3] == "UNC": #Username change
                    self._username = message[4:]  
                elif message[:3] == "UNP": #Password change
                    self._password = message[4:]
                elif message[:3] == "HSC": #Hash change
                    self._lastHash = message[4:]
            
            #If timeout expired, check for new notes
            if not ((self._username == "") or (self._password == "") or (self._verifyAuto == 0)):
                if (lastCheck + (self._verifyTimeout*60)) < time.time():
                    try:
                        print "Checking..."
                        response = ""
                        Pagina = http.Page("http://www.sigmawebplus.com.br/server/")
                        Pagina.set_RequestHeaders(http.Header("username", self._username), http.Header("password", self._password), http.Header("hash", self._lastHash))
                        Pagina.Refresh()
                        response = Pagina.get_ResponseData()
                    except:
                        pass
                    
                    #Avalia resposta
                    if not (response[:10] == "Up-to-date"):
                        
                        #Se nao for a primeira vez que esta sendo feita a busca, joga uma notificacao
                        if self._lastHash <> "":
                            Notification("SigmaWeb+","Novas notas disponiveis!").notify()
                        
                        #Salva a nova hash
                        self._lastHash = response[:32]
                        
                        #Manda as informacoes para o App exibir na tela
                        ThreadComm.sendMsg("NNA "+response)
                        
                    
                    lastCheck = time.time()

            time.sleep(1)
        
        Debug().log("Monitor: Killed successfully")
    
    def kill(self):
        self._exit = True

if __name__ == '__main__':
    #On Android platform this code is executed automaticaly
    Service().run()