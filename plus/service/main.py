from threadcomm import ThreadComm, ThreadCommException, ThreadCommServer
from debug import Debug
from time import time, sleep
from http import Page, Header
from datetime import datetime
from notification.notification import Notification

class MainService:
    CONFIG_THREADCOMMPORT = 51352
    CONFIG_THREADCOMMID = "sigmawebplus"
    
    SIGTERM = False
    SIGSTRT = False
    data = None
    
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
        
        while (self.SIGTERM==False):
            self.listen()
            if self.SIGSTRT: self.check()
            sleep(0.1)
        
        try: self.threadComm.sendMsg("STOP")
        except: Debug().error("Unable to send ThreadComm message with 'STOP' signal in MainService.run()", "Service")
        self.threadComm.stop()
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
    
    def check(self):
        if (self.getKey('username') <> ''):
            if (float(self.getKey('update_time'))+float(self.getKey('update_timeout'))*60 < time()) or (self.getKey('update_force')=='1'):
                Debug().note("Buscando notas no server...", "Service")
                try:
                    pagina = Page("http://www.sigmawebplus.com.br/server/")
                    pagina.set_RequestHeaders(Header("username", self.getKey('username')), Header("password", self.getKey('password')), Header("hash", self.getKey('update_hash')), Header("version", self.getKey('app_version')))
                    pagina.Refresh()
                    response = pagina.get_ResponseData()
                except: response = ''
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
                        self.setKey('update_msg', "Erro: Tente novamente mais tarde")
                elif response[:10] == "Up-to-date":
                    Debug().note("Resposta do server 'Up-to-date'", "Service")
                    self.setKey('update_msg', "Ultima atualizacao em "+str(datetime.fromtimestamp(time()).strftime('%d/%m/%y %H:%M')))
                elif response[33:(33+10)] == "<SigmaWeb>":
                    if self.getKey('update_hash') != '': Notification('Novos resultados disponiveis', "Atualizado as "+str(datetime.fromtimestamp(time()).strftime('%H:%M'))).notify()
                    hash = response[:32]
                    data = response[33:]
                    self.setKey('update_msg', "Ultima atualizacao em "+str(datetime.fromtimestamp(time()).strftime('%d/%m/%y %H:%M')))
                    self.setKey('update_hash', hash)
                    self.setKey('update_data', data)
                    Debug().note("Resposta do server '"+hash+"'", "Service")
                else:
                    Debug().error("Erro ao requisitar notas!", "Service")
                    self.setKey('update_msg', "Erro: Tente novamente mais tarde")
                
                self.setKey('update_time', time())
    
    def getKey(self, key):
        try: value = str(self.data[key])
        except: value = ''
        return value
    
    def setKey(self, key, value):
        self.data[key] = str(value)
        self._sendKey(key)
    
    def _sendKey(self, key):
        try: value = str(self.data[key])
        except: value = ''
        length = str(len(key)).zfill(2)
        try: self.threadComm.sendMsg("SKEY"+length+key+value)
        except: Debug().warn("Unable to send ThreadComm message with key '"+key+"' in MainService._sendKey()", "Service")
                
if __name__ == '__main__':
    MainService().run()