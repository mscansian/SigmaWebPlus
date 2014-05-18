import time, http

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
    _username = None
    _password = None
    _lastHash = None
    
    def run(self):        
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
            Debug().log("Service running...")
            
            #Check for ThreadComm messages
            message = ThreadComm.recvMsg()
            if message <> None:
                print "Service RCV: "+message
                if message[:3] == "TOC": #Timeout change
                    self._verifyTimeout = message[4:]
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
            
            print self._verifyTimeout
            
            #If timeout expired, check for new notes
            if self._username == None or self._password == None:
                if (lastCheck + (self._verifyTimeout*60)) < time.time():
                    try:
                        Pagina = http.Page("https://drpexe.com/scripts/sigmawebplus2/")
                        Pagina.set_RequestHeaders(http.Header("username", self._username), http.Header("password", self._password), http.Header("hash", self._lastHash))
                        Pagina.Refresh()
                        Debug().log( Pagina.get_ResponseData())
                    except:
                        pass
                    lastCheck = time.time()

            time.sleep(0.1)
        
        Debug().log("Monitor: Killed successfully")
    
    def kill(self):
        self._exit = True

if __name__ == '__main__':
    #On Android platform this code is executed automaticaly
    Service().run()