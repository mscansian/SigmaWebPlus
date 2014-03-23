from Singleton import Singleton
import kivy_notification

class EventHandler():
    _Dispatcher = None
    
    #Use singleton for the event handler
    __metaclass__ = Singleton
    
    def __init__(self, dispatcher=None):
        if dispatcher <> None:
            self._Dispatcher = dispatcher
            
    def onButtonConfigPress(self, instance):
        self._Dispatcher.openSettings()
        
    def onButtonUpdatePress(self, instance):
        kivy_notification.Notification("Button Pressed", "Update").notify()
    
    