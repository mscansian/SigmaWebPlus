#!/usr/bin/python
# -*- coding: UTF-8 -*-

from kivy.utils import platform
from kivyapp import KivyApp
from service import ServiceLaucher
from service.threadcomm.threadcomm import ThreadComm, ThreadCommException, ThreadCommClient
from singleinstance.singleinstance import SingleInstance
import events 

class SigmaWeb:
    #Constants
    CONFIG_SINGLEINSTANCEPORT = 50363
    CONFIG_THREADCOMMPORT = 51352
    CONFIG_THREADCOMMID = " sigmawebplus"
    
    #Objects
    singleInstance = None
    kivy = None
    threadComm = None
    service = None
    
    #Variables
    oldServiceData = None
    
    '''
    ''   APP INITIALIZATION
    '''
    
    def __init__(self):
        pass

    def run(self):
        self.on_start()
    
    def on_start(self):     
        #Creates a handle for SingleInstance (this is not necessary on Android 'cause the OS takes care of this!
        if platform <> 'android':
            self.singleInstance = SingleInstance(self.CONFIG_SINGLEINSTANCEPORT, False)
        
        #Load Service
        self.service = ServiceLaucher()
        serviceAlive = self.isServiceAlive()
        
        if (not serviceAlive):
            #Start service
            self.service.start()
            
            #Connect Threadcomm
            while True: #
                try: self.threadComm.start()
                except ThreadCommException: pass
                else: break
        
        #Subscribe to events
        events.Events().subscribe(events.EVENT_RELOAD, self.on_event_reload)
        events.Events().subscribe(events.EVENT_CONFIGCHANGE, self.on_event_configchange)
        events.Events().subscribe(events.EVENT_LOGIN, self.on_event_login)
        events.Events().subscribe(events.EVENT_WRONGPASSWORD, self.on_event_wrongpassword)
        events.Events().subscribe(events.EVENT_APPSTART, self.on_event_appstart)
        events.Events().subscribe(events.EVENT_APPEND, self.on_event_append)
        events.Events().subscribe(events.EVENT_KIVYUPDATE, self.update)
        
        #Load and start kivy
        self.kivy = KivyApp()
        self.kivy.run()
        
    def isServiceAlive(self):
        #Load ThreadComm and check if service is running
        self.threadComm = ThreadComm(self.CONFIG_THREADCOMMPORT, self.CONFIG_THREADCOMMID, ThreadCommClient)
        try: self.threadComm.start()
        except ThreadCommException: return False #Service is not running
        else:
            #Service is running. Get all info from server and ask to shutdown
            self.threadComm.sendMsg("RFS")
            self.oldServiceData = []
            while True:
                try:
                    message = self.threadComm.recvMsg()
                except ThreadCommException: pass
                else:
                    if message[:3] == "RF1":
                        self.oldServiceData.append(message[4:]) #update_time: Last time the data was updated
                    elif message[:3] == "RF2":
                        self.oldServiceData.append(message[4:(32+4)]) #update_hash: The hash of last update
                        self.oldServiceData.append(message[(32+5):])  #update_data: The data of last update
                        return True #Service is running!

    '''
    ''   APP FINALIZATION
    '''
    
    def on_stop(self, shutdownService):
        if platform <> 'android': self.singleInstance.kill()
        print shutdownService
        if shutdownService:
            try: self.threadComm.sendMsg("KIL")
            except Exception as e: print "Warning [self.threadComm.sendMsg(\"KIL\")]: "+str(e)
            try: self.service.kill()
            except Exception as e: print "Warning [self.service.kill()]: "+str(e)
        self.threadComm.stop()
    
    '''
    ''   MAIN UPDATE
    '''
    
    def update(self, *args):
        #Check if oldServiceData contains information
        if self.oldServiceData <> None:
            events.Events().trigger(events.EVENT_UPDATEDATA, *self.oldServiceData) #Trigger kivy event to update data
            self.oldServiceData = None
        
        try:
            message = self.threadComm.recvMsg()
        except ThreadCommException as e:
            pass
        else:
            if message[:3] == "NNA": #New Notas Available
                #Parse the information
                time = message[4:(10+4)] #Beware: This will stop working on 20 Nov 2286!!!!!
                hash = message[(10+4):(32+10+4)]
                data = message[(32+10+4+1):]
                events.Events().trigger(events.EVENT_UPDATEDATA, time, hash, data) #Trigger kivy event to update data
            elif message[:3] == "UTD":
                events.Events().trigger(events.EVENT_UPTODATE, message[4:])
            elif message[:3] == "ERR": #Erro no servidor
                if message[4:] == "Auth error":
                    events.Events().trigger(events.EVENT_WRONGPASSWORD)
                else:
                    events.Events().trigger(events.EVENT_SERVERERROR)

    '''
    ''   EVENT HANDLER
    '''
    
    def on_event_reload(self, *args):
        self.threadComm.sendMsg("CKN")
        
    def on_event_configchange(self, *args):
        config, section, key, value = args
        if key == 'update_timeout':
            self.threadComm.sendMsg("TOC "+str(value))
        elif key == 'update_auto':
            self.threadComm.sendMsg("ATC "+str(value))
        elif (key == 'app_delete') and (value =='1'):
            self.kivy.stop()
    
    def on_event_login(self, *args):
        self.threadComm.sendMsg("UNC "+args[0])
        self.threadComm.sendMsg("UNP "+args[1])
        self.threadComm.sendMsg("CKN")
    
    def on_event_wrongpassword(self, *args):
        self.threadComm.sendMsg("UNC ")
        self.threadComm.sendMsg("UNP ")
    
    def on_event_appstart(self, *args):
        time, hash, data, timeout, auto = args
        self.threadComm.sendMsg("LCK "+time)
        self.threadComm.sendMsg("HSC "+hash)
        self.threadComm.sendMsg("SUD "+hash.rjust(32)+"\n"+data)
        self.threadComm.sendMsg("TOC "+timeout)
        self.threadComm.sendMsg("ATC "+auto)
    
    def on_event_append(self, *args):
        self.on_stop(*args)    

if __name__ == '__main__':
    SigmaWeb().run()