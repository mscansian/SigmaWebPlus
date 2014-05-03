import time, http

from kivy.logger import Logger
from kivy.utils import platform
from notification_demo.components.notification import Notification


if platform <> "android":
    from service.debug import Debug
else:
    from debug import Debug

class Monitor():
    _verifyTimeout = 10 #Seconds
    _exit = False
    
    def run(self):        
        Debug().log("Monitor: Started successfully")
        
        #Start ThreadComm
        try:
            import threadcomm
            ThreadComm = threadcomm.ThreadComm(51352, "sigmawebplus")
        except threadcomm.ThreadCommException as e:
            sys.exit(e.value)
        
        #Run until SIGTERM
        lastCheck = 0
        while (self._exit==False):
            Debug().log("Service running...")
            
            #Check for ThreadComm messages
            message = ThreadComm.recvMsg()
            if message <> None:
                if message[:3] == "TOC": #Timeout change
                    self._verifyTimeout = message[4:]
                elif message[:3] == "CKN": #Check now
                    lastCheck = 0
                elif message[:3] == "KIL": #Kill
                    self._exit = True
            
            #If timeout expired, check for new notes
            if (lastCheck + self._verifyTimeout) < time.time():
                Notification("Verificando pagina...", "Servico").notify()
                Pagina = http.Page("https://scripts.drpexe.com")
                Pagina.set_RequestHeaders(http.Header("User-Agent", "SigmaWebPlus"), http.Header("Connection", "Close"))
                Pagina.Refresh()
                Debug().log( Pagina.get_ResponseData())
                lastCheck = time.time()
            
            time.sleep(1)
        
        Debug().log("Monitor: Killed successfully")
    
    def kill(self):
        self._exit = True

if __name__ == '__main__':
    #On Android platform this code is executed automaticaly
    Monitor().run()
        
        
        
        

    #import http

    #Pagina = http.Page("https://www.math.unl.edu/~shartke2/computer/phpinfo.php")
    #Pagina.set_RequestHeaders(http.Header("User-Agent", "meuvalor"), http.Header("Connection", "Close"))
    #Pagina.Refresh()

    #for header in Pagina.get_ResponseCookies():
    #    print header.get_Name() + " -> "+header.get_Value()

    #print Pagina.get_ResponseData()