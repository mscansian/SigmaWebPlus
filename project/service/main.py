import time
import kivy.lib.osc
import plyer

if __name__ == '__main__':
    OSC = kivy.lib.osc.init()

    print "fim"

    while True:
        print "*********  service rodando **********************"
        time.sleep(3)
        
        
        
        

    #import http

    #Pagina = http.Page("https://www.math.unl.edu/~shartke2/computer/phpinfo.php")
    #Pagina.set_RequestHeaders(http.Header("User-Agent", "meuvalor"), http.Header("Connection", "Close"))
    #Pagina.Refresh()

    #for header in Pagina.get_ResponseCookies():
    #    print header.get_Name() + " -> "+header.get_Value()

    #print Pagina.get_ResponseData()