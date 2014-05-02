import time

#Custom
from debug import Debug

class Monitor():
    _exit = False
    
    def run(self):        
        #Setup OSC
        print "Stating OSC"
        try:
            import threadcomm
            ThreadComm = threadcomm.ThreadComm(51352, "sigmawebplus")
        except threadcomm.ThreadCommException as e:
            sys.exit(e.value)
        
        while (self._exit==False):
            Debug().log("Thread running...")
            msg = ThreadComm.recvMsg()
            if msg <> None:
                print "Service msg: " + msg
            ThreadComm.sendMsg("asdadsadas")
            #print "send msg"
            time.sleep(1)
        
        print "Monitor: Shutting down OSC"
        
        print "Monitor: OSC is down!"
        
        Debug().log("Monitor: Killed successfully")
    
    def kill(self):
        print "Monitor: SIGTERM received"
        self._exit = True
    
    def receiveMessage(self, message, *args):
        print "Received: "+message

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