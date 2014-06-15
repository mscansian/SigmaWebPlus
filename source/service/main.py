#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time, http, random

from kivy.logger import Logger
from kivy.utils import platform
from notification_demo.components.notification import Notification
from threadcomm import threadcomm


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
    
    def run(self):
        Debug().log("Monitor: Started successfully")
        
        #Start ThreadComm
        ThreadComm = threadcomm.ThreadComm(51353, "sigmawebplus", threadcomm.ThreadCommServer)
        ThreadComm.start()
        
        #Run until SIGTERM
        lastCheck = 0
        while (self._exit==False):
            
            #Check for ThreadComm messages
            try:
                message = ThreadComm.recvMsg()
            except:
                pass
            else:
                print "-------------Service RCV: "+message
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
                        print "Debug: Fetching data from server..."
                        response = ""
                        Pagina = http.Page("http://www.sigmawebplus.com.br/server/")
                        Pagina.set_RequestHeaders(http.Header("username", self._username), http.Header("password", self._password), http.Header("hash", self._lastHash))
                        Pagina.Refresh()
                        response = Pagina.get_ResponseData()
                    except:
                        print "Warning: Failed to fetch data from server"
                    
                    #Avalia resposta
                    if response[:7] == "<error>":
                        print "Warning: Server returned an error '"+response[7:-8]+"'"
                        ThreadComm.sendMsg("ERR "+response[7:-8])
                    elif response[:10] == "Up-to-date":
                        print "Debug: Data is up-to-date"
                        ThreadComm.sendMsg("UTD ")
                    else:
                        #Se nao for a primeira vez que esta sendo feita a busca, joga uma notificacao
                        if self._lastHash <> "":
                            Notification("SigmaWeb+","Novas notas disponiveis!").notify()
                        
                        #Salva a nova hash
                        self._lastHash = response[:32]
                        
                        #Manda as informacoes para o App exibir na tela
                        try:
                            print "Send"
                            ThreadComm.sendMsg("NNA "+response)
                        except:
                            print "Warning: Unable to send new data to main.py in service/main.py"
                        
                    
                    lastCheck = time.time()

            time.sleep(1)
        
        Debug().log("Monitor: Killed successfully")
    
    def kill(self):
        self._exit = True

if __name__ == '__main__':
    #On Android platform this code is executed automaticaly
    Service().run()