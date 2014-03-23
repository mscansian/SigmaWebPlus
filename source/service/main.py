import time
from kivy.lib import osc
import plyer

def receive_msg(message, *args):
    print "Received "+message

def main(parameters=None):
    osc.init()
    oscid = osc.listen(ipAddr='127.0.0.1', port=3001)
    osc.bind(oscid, receive_msg, '/some_api')

    print "fim"

    while True:
        osc.readQueue(oscid)
        time.sleep(.5)

if __name__ == '__main__':
    main()
        
        
        
        

    #import http

    #Pagina = http.Page("https://www.math.unl.edu/~shartke2/computer/phpinfo.php")
    #Pagina.set_RequestHeaders(http.Header("User-Agent", "meuvalor"), http.Header("Connection", "Close"))
    #Pagina.Refresh()

    #for header in Pagina.get_ResponseCookies():
    #    print header.get_Name() + " -> "+header.get_Value()

    #print Pagina.get_ResponseData()