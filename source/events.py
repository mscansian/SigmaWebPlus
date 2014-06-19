import Singleton

#Event constants - I am doing this because enum is not supported on python2.7
EVENT_RELOAD        = 1  #Fired when user clicks on Update button
EVENT_LOGIN         = 2  #Fired when user click on Login button
EVENT_WRONGPASSWORD = 3  #Fired when server return a 'Wrong Password' error
EVENT_CONFIGCHANGE  = 4  #Fired when a config on kivy.ini changes
EVENT_APPSTART      = 5  #Fired when the app is started
EVENT_APPEND        = 6  #Fired when the app is about to end
EVENT_APPPAUSE      = 7  #Fired when the app is paused
EVENT_APPRESUME     = 8  #Fired when the app is resumed
EVENT_UPDATEDATA    = 9  #Fired when the server returns new data
EVENT_UPTODATE      = 10 #Fired when server return Up-to-date message
EVENT_SERVERERROR   = 11 #Fired when server returns a custom error (not AuthFailed)
EVENT_KIVYUPDATE    = 12 #Fired when kivy updates a frame

class Events:    
    #Variables
    subscribers = None
    
    #Singleton
    __metaclass__ = Singleton.Singleton
    
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, eventType, callback):
        try:
            #Get list of current subscribers
            currentSubscribers = self.subscribers[eventType]
        except KeyError: #Create a new subscriber list if it does not exist
            currentSubscribers = []
            
        #Register a new subscriber and save list
        currentSubscribers.append(callback)
        self.subscribers[eventType] = currentSubscribers
    
    def trigger(self, eventType, *args):
        try:
            #Get list of current subscribers
            currentSubscribers = self.subscribers[eventType]
        except KeyError:
            currentSubscribers = []
        
        #For each subscriber, trigger the callback function
        for subscriber in currentSubscribers:
            subscriber(*args)
