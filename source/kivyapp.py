#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import kivy.app
import kivy.config
import kivy.utils
import kivy.clock

import serverXMLparser, layout, events

class KivyApp(kivy.app.App):
    #Objects
    GUI = None 
    
    #Kivy Configuration
    use_kivy_settings = False

    '''
    ''   APP INITIALIZATION
    '''
 
    #Override methods
    def build(self):
        #Load GUI
        self.GUI = layout.GUI()
        self.root = self.GUI.root
        
        kivy.clock.Clock.schedule_interval(self.update, 0) #Schedule main update
         
    def on_start(self):
        self.userConfig.setConfig('app_delete', '0') #Hack
        
        #Subscribe to events
        events.Events().subscribe(events.EVENT_RELOAD, self.on_event_reload)
        events.Events().subscribe(events.EVENT_LOGIN, self.on_event_login)
        events.Events().subscribe(events.EVENT_WRONGPASSWORD, self.on_event_wrongpassword)
        events.Events().subscribe(events.EVENT_UPDATEDATA, self.on_event_updatedata)
        events.Events().subscribe(events.EVENT_UPTODATE, self.on_event_uptodate)
        
        self.GUI.setWindow(layout.screenLogin) #Carrega janela de login
        events.Events().trigger(events.EVENT_LOGIN, *self.userConfig.getLogin()) #Tenta realizar o login
        
        self.update()
        events.Events().trigger(events.EVENT_UPDATEDATA, *self.userConfig.getUserData())
        events.Events().trigger(events.EVENT_APPSTART, *(self.userConfig.getUserData() + self.userConfig.getUserConfig()))

    '''
    ''   APP LIFE CYCLE
    '''

    def on_stop(self):
        shutdownService = True if (self.GUI.getWindow()==layout.screenLogin) else False
        events.Events().trigger(events.EVENT_APPEND, shutdownService)
        
    def on_pause(self):
        if self.GUI.getWindow() == layout.screenLogin: #If app is on Login screen, then closes everything
            return False
        else:
            return True
    
    def on_resume(self):
        pass
    
    '''
    ''   OTHERS
    '''
    
    def update(self, *args):
        events.Events().trigger(events.EVENT_KIVYUPDATE, *args)
    
    def build_settings(self, settings):
        jsondata = open('config.json', 'r').read()
        settings.add_json_panel('SigmaWeb+', self.config, data=jsondata)

    '''
    ''   CONFIGURATION RELATED
    '''


    def build_config(self, config):
        #Initiate Userconfig object
        self.userConfig = Userconfig(config)
        
        #Set some kivy options
        #Todo: Check if this is working (I don't think so)
        kivy.Config.set('kivy', 'exit_on_escape', 0)
        kivy.Config.set('kivy', 'log_enable', 0)

    def on_config_change(self, config, section, key, value):
        self.userConfig.on_change(config, section, key, value) #Forward to userConfig
    
    '''
    ''   EVENT HANDLING
    '''
    
    #Converts events from .kv format to the classes format
    def event_converter(self, eventType, *args):
        if eventType == "VerificarNotas":
            events.Events().trigger(events.EVENT_RELOAD, *args)
        elif eventType == "Login":
            events.Events().trigger(events.EVENT_LOGIN, *args)
    
    def on_event_reload(self, *args):
        pass #Colocar uma mensagem na tela de 'Carregando notas'
    
    def on_event_login(self, *args):
        if not ((args[0] == "") or (args[1]=="")):
            self.userConfig.setLogin(*args)
            self.GUI.setWindow(layout.screenMain)
    
    def on_event_wrongpassword(self, *args):
        self.userConfig.clearLogin()            
        self.GUI.setWindow(layout.screenLogin)
    
    def on_event_updatedata(self, *args):
        time, hash, data = args
        self.userConfig.setUserData(*args)
        alunoObject = serverXMLparser.alunoXML(*args) if (data<>'') else None #Faz um parse do codigo XML para mostrar as notas
        self.GUI.setNotas(alunoObject) #Modifica pagina mostrando as notas
    
    def on_event_uptodate(self, *args):
        self.userConfig.setUserDataTime(args[0])
        time, hash, data = self.userConfig.getUserData()
        alunoObject = serverXMLparser.alunoXML(*self.userConfig.getUserData()) if (data<>'') else None #Faz um parse do codigo XML para mostrar as notas
        self.GUI.setNotas(alunoObject) #Modifica pagina mostrando as notas
    
class Userconfig:
    #Hard coded config
    defaultSection = 'Sigmauser'
    defaultConfig = {
                     'username': '',
                     'password': '', 
                     'update_timeout': '60', 
                     'update_time': '0', 
                     'update_hash': '', 
                     'update_auto': '1', 
                     'update_data': '', 
                     'app_delete': '0'
                     }
    
    
    configObject = None
    changeCallback = None
    
    def __init__(self, configObject):
        self.configObject = configObject
        self.configObject.setdefaults(self.defaultSection,self.defaultConfig)
    
    def clearAll(self):
        self.clearLogin()
        self.clearUserData()
    
    def setLogin(self, username, password):
        self.setConfig('username', username)
        self.setConfig('password', password)
    
    def getLogin(self):
        return [
                self.getConfig('username'),
                self.getConfig('password')
                ]
    
    def clearLogin(self):
        self.setLogin('', '')
    
    def setUserDataTime(self, time):
        self.setConfig('update_time', time)
        
    def setUserData(self, time, hash, data):
        self.setConfig('update_time', time)
        self.setConfig('update_hash', hash)
        self.setConfig('update_data', data)
    
    def getUserData(self):
        return [
                self.getConfig('update_time'),
                self.getConfig('update_hash'),
                self.getConfig('update_data')
                ]
    
    def getUserConfig(self):
        return [
                self.getConfig('update_timeout'),
                self.getConfig('update_auto')
                ]
    
    def clearUserData(self):
        self.setUserData('0', '', '')
        
    def setConfig(self, key, value):
        #Change configuration and write to file
        self.configObject.set(self.defaultSection,key, value)
        self.configObject.write()
        
        self.on_change(self.configObject, self.defaultSection, key, value)
    
    def getConfig(self, key):
        return self.configObject.get(self.defaultSection, key)
    
    def on_change(self, config, section, key, value):
        if (config==self.configObject) and (section==self.defaultSection) and (key=='app_delete') and (value=='1'):
            self.clearAll()
        
        events.Events().trigger(events.EVENT_CONFIGCHANGE, config, section, key, value) #Forward to event handler