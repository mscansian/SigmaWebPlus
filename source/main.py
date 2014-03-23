print "inicio porra"

from kivy.utils import platform
import sys
from service.debug import Debug

#Program entry point
if __name__ == '__main__':
    if platform <> 'android':
        try:
            import singleinstance
            PythonInstance = singleinstance.SingleInstance(51361, False)
        except singleinstance.SingleInstanceException as e:
            sys.exit(e.value)
    
    print "Criando monitor..."
    import service
    #try:
        #monitor = service.MonitorLaucher()
    #except:
    #    raise
    
    from app import SigmaWebApp
    
    while True:
        SigmaWebApp().run()
        if platform == 'android':
            #In android platform is safe to leave (the system will keep the service running)
            break
        else:
            #We should ensure that the service is still running
            break #Todo
    
    Debug().log("Exiting the main program...")
    PythonInstance.kill()
    #monitor.kill()
    sys.exit(0)