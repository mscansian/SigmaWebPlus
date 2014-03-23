#System libs
import time, sys

#Custom
import kivy.utils
from debug import Debug


class Monitor():
    parameters = None
    thread = None
    exit = False
    
    def start(self, parameters=None):
        Debug().log("Monitor inicializado. Configurando...")
        self.parameters = parameters
        if kivy.utils.platform == 'android': #Run program
            self.run()
        else: #Set up thread
            Debug().log("Criando thread para o monitor")
            import threading
            try:
                self.thread = threading.Thread(target=self.run)
                self.thread.daemon = False
                self.thread.start()
            except:
                Debug().log("Erro ao criar o thread para o monitor")
                sys.exit(1)
                
    def run(self):
        import plyer
        from kivy.lib import osc
        
        #Setup OSC
        print "Monitor: Iniciando OSC"
        osc.init()
        self.oscid = osc.listen(ipAddr='127.0.0.1', port=3001)
        osc.bind(self.oscid, self.receiveMessage, '/sigmawebplus')
        
        while (self.exit==False):
            Debug().log("Thread running...")
            osc.readQueue(self.oscid)
            time.sleep(2)
            
        Debug().log("Exiting thread")
    
    def kill(self):
        self.exit = True
    
    def receiveMessage(self, message, *args):
        print "Received: "+message

if __name__ == '__main__':
    Monitor().run()
        
        
        
        

    #import http

    #Pagina = http.Page("https://www.math.unl.edu/~shartke2/computer/phpinfo.php")
    #Pagina.set_RequestHeaders(http.Header("User-Agent", "meuvalor"), http.Header("Connection", "Close"))
    #Pagina.Refresh()

    #for header in Pagina.get_ResponseCookies():
    #    print header.get_Name() + " -> "+header.get_Value()

    #print Pagina.get_ResponseData()