import time

#Custom
from debug import Debug
from kivy.lib import osc

class Monitor():
    exit = False
    
    def run(self):        
        #Setup OSC
        print "Monitor: Iniciando OSC"
        osc.init()
        self.oscid = osc.listen(ipAddr='127.0.0.1', port=3001)
        osc.bind(self.oscid, self.receiveMessage, '/sigmawebplus')
        osc.sendMsg("/sigmawebplus")
        
        while (self.exit==False):
            Debug().log("Thread running...")
            osc.readQueue()
            time.sleep(1)
        
        print "4"
        
        osc.dontListen()
        print "5"
        Debug().log("Monitor: Killed successfully")
    
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