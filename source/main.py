print "Starting /main.py"

from kivy.utils import platform
import sys
from service.debug import Debug

#Program entry point
if __name__ == '__main__':
    if platform <> 'android':
        #Creates a handle for SingleInstance (this is not necessary on Android 'cause the OS takes care of this!
        try:
            from singleinstance import singleinstance
            PythonInstance = singleinstance.SingleInstance(50362, True)
        except singleinstance.SingleInstanceException as e:
            sys.exit(e.value)
    
    #Monitor
    import service
    try:
        AppMonitor = service.MonitorLaucher()
    except:
        raise #your hands
    
    from app import SigmaWebApp
    
    while True:
        #Run main app and hold until 'SIGTERM' is raised
        SigmaWebApp().run()
        
        #Closing application
        if platform == 'android':
            #In android platform is safe to leave (the system will keep the service running)
            break
        else:
            #We should ensure that the service is still running
            break #Todo
    
    #Cleaning up the mess
    Debug().log("Exiting the main program...")
    if platform <> 'android':
        AppMonitor.kill()
        PythonInstance.kill()
    sys.exit(0)