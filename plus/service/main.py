#!/usr/bin/python
# -*- coding: UTF-8 -*-

from types import *
from threading import Thread
from time import time, sleep
from datetime import datetime

from kivy.utils import platform
from threadcomm import ThreadComm, ThreadCommException, ThreadCommServer
from notification.notification import Notification

from debug import Debug
from http import Page, Header

class MainService:
    CONFIG_THREADCOMMPORT = 51352
    CONFIG_THREADCOMMID = "sigmawebplus"
    
    SIGTERM = False
    SIGSTRT = False
    data = None
    
    '''
    Essas variaveis sao utilizadas para o service avisar o main thread para lancar uma notification
    Nota: No android soh o main thread pode fazer notification
    '''
    androidService = False
    notificationMsg = None 
    
    threadComm = None
    
    def init(self):
        Debug().note("Started successfully", "Service")
        
        #Configuracoes
        self.data = {}
        
        #Start ThreadComm
        self.threadComm = ThreadComm(self.CONFIG_THREADCOMMPORT, self.CONFIG_THREADCOMMID, ThreadCommServer)
        self.threadComm.start()
        Debug().note("ThreadComm started", "Service")
    
    def run(self):
        self.init()
        
        '''
        Main loop do Sevice. O objetivo do try/except é se algum erro acontecer, ele limpa
            a memoria e então da re-raise
        '''
        while (self.SIGTERM==False):
            try:
                self.listen()
                if self.SIGSTRT: self.check()
                sleep(0.1)
            except:
                Debug().error("Erro fatal! Tentando limpar a memória antes de sair...", "Service")                
                self._cleanResources()
                raise
        
        self._cleanResources()
        Debug().note("Ended successfully", "Service")
    
    def listen(self):
        #Check for ThreadComm messages
        while True:
            try: message = self.threadComm.recvMsg()
            except: break
            
            if message[:4] == "SKEY": #Set key
                length = int(message[4:6])
                key = message[6:6+length]
                value = message[6+length:]
                self.data[key] = value
            elif message[:4] == "GKEY": #Get key
                key = message[4:]
                self._sendKey(key)
            elif message[:4] == "AKEY": #Get all keys
                for key in self.data:
                    self._sendKey(key)
            elif message[:4] == "KILL": #Kill service
                self.SIGTERM = True
            elif message[:4] == "STRT": #Start service
                self.SIGSTRT = True
                self.threadComm.sendMsg("STRT")
    
    def check(self):
        update_timeout = float(self.getKey('update_timeout'))
        update_time = float(self.getKey('update_time'))
        if (update_timeout < 30): self.setKey('update_timeout', '30')
        
        shouldCheck = ((update_time+update_timeout*60 < time()) or (self.getKey('update_force')=='1')) and (self.getKey('username') <> '') 
        if shouldCheck:
            
            Debug().note("Buscando notas no server...", "Service")
            try:
                pagina = Page("http://www.sigmawebplus.com.br/server/")
                pagina.set_RequestHeaders(Header("username", self.getKey('username')), Header("password", self.getKey('password')), Header("hash", self.getKey('update_hash')), Header("version", self.getKey('app_version')), Header("force", self.getKey('update_force')), Header("timeout", self.getKey('update_timeout')), Header("auto", self.getKey('update_auto')))
                pagina.Refresh()
                response = pagina.get_ResponseData()
                if self.getKey('debug_serverout') == '1': Debug().data(response, "Server response")
            except: response = ''
            assert type(response) is StringType
            if self.getKey('update_force') == '1': self.setKey('update_force', '0')
            
            if response[:7] == "<error>":
                error = response[7:-8]
                Debug().warn("Resposta do server error('"+error+"')", "Service")
                if (error == "Auth error") or (error == "Username or password blank"):
                    self.setKey('username', '')
                    self.setKey('password', '')
                    self.setKey('update_time', '0')
                    return False
                else:
                    self.setKey('update_msg', "Erro no servidor!\nTente novamente mais tarde")
            elif response[:10] == "Up-to-date":
                Debug().note("Resposta do server 'Up-to-date'", "Service")
                self.setKey('update_msg', "Ultima atualizacao em "+str(datetime.fromtimestamp(time()).strftime('%d/%m/%y %H:%M:%S')))
            elif response[33:(33+10)] == "<SigmaWeb>":
                hash = response[:32]
                data = response[33:]
                
                if self.getKey('update_hash') != '': #Se esta nao eh a primeira vez que o usuario busca nota
                    self._notify()
                
                self.setKey('update_msg', "Ultima atualizacao em "+str(datetime.fromtimestamp(time()).strftime('%d/%m/%y %H:%M:%S')))
                self.setKey('update_hash', hash)
                self.setKey('update_data', data)
                Debug().note("Resposta do server '"+hash+"'", "Service")
            else:
                Debug().error("Erro ao requisitar notas!", "Service")
                self.setKey('update_msg', "Erro no servidor!\nTente novamente mais tarde")
            
            self.setKey('update_time', time())
    
    def getKey(self, key):
        try: value = str(self.data[key])
        except: value = ''
        return value
    
    def setKey(self, key, value):
        self.data[key] = str(value)
        self._sendKey(key)
    
    def _notify(self):
        notificationMsg = ['Novos resultados disponiveis', "Atualizado as "+str(datetime.fromtimestamp(time()).strftime('%H:%M'))]
        if platform != 'android': 
            Notification(*notificationMsg).notify()
        else:
            '''
            O android tem algumas frescuras em relacao a API de notificacoes:
                A notificacao soh pode ser chamada pelo main thread e existe libs diferentes para quando
                um service ou uma activity chama a notificacao
            O codigo abaixo verifica se este objeto esta sendo executado como service do android ou thread
                Se for um service do android. Ele seta uma flag para o main thread do service chamar a notificacao
                Se for um thread comum, ele manda uma mensagem (NOTI) para o main thread do app chamar a notificacao
            '''
            if not self.androidService: 
                try: self.threadComm.sendMsg("NOTI"+notificationMsg[0]+"|"+notificationMsg[1])
                except: Debug().warn("Unable to send ThreadComm message with notification request in MainService._notify()", "Service")
            else:
                self.notificationMsg = notificationMsg
    
    def _sendKey(self, key):
        try: value = str(self.data[key])
        except: value = ''
        length = str(len(key)).zfill(2)
        try: self.threadComm.sendMsg("SKEY"+length+key+value)
        except: Debug().warn("Unable to send ThreadComm message with key '"+key+"' in MainService._sendKey()", "Service")
    
    def _cleanResources(self):
        try: self.threadComm.sendMsg("STOP")
        except: Debug().error("Unable to send ThreadComm message with 'STOP' signal in MainService.run()", "Service")
        self.threadComm.stop()
    
if __name__ == '__main__':
    ''' 
    O service no android roda no main thread. O objetivo do codigo abaixo eh forcar ele
    a rodar em um thread separado
    '''
    serviceObject = MainService()
    serviceObject.androidService = True
    serviceThread = Thread(target=serviceObject.run, name='MainService')
    serviceThread.start()
    
    '''
    Continua funcionando ateh que o Thread seja finalizado
    Isso eh necessario pq o Android soh deixa o Main Thread fazer notificacoes.
    O codigo dentro do loop cuida disso
    '''
    while serviceThread.is_alive():
        if serviceObject.notificationMsg is not None: 
            Notification(*serviceObject.notificationMsg).notify()
            serviceObject.notificationMsg = None
            
    