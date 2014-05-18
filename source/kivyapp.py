#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import kivy.app
import kivy.config
import kivy.utils
import kivy.clock

import layout
from service.debug import Debug

class KivyApp(kivy.app.App):
    _GUI = None
    
    _callback_update = None
    _callback_configchange = None
    _callback_programexit = None
    _callback_notasrequested = None
    
    #Kivy app config
    config_username = None
    config_password = None
    config_timeout = None
    
    #Kivy Configuration
    use_kivy_settings = False

    #Custom methods
    def changeWindow(self, window):
        self._GUI.change(window)
        self.root = self._GUI.getRoot()
    
    def setCallbacks(self, update, configchange, programExit, notasreq):
        self._callback_update = update
        self._callback_configchange = configchange
        self._callback_programexit = programExit
        self._callback_notasrequested = notasreq
    
    def updateNotas(self, notas):
        pass
    
    #GUI callbacks
    def callback_VerifyNotas(self, *args):
        self._callback_notasrequested()
    
    def callback_Configuracoes(self, *args):
        self.open_settings()
    
    def callback_Login(self, *args):
        pass
        
    #Override methods
    def build(self):
        #Load GUI
        self._GUI = layout.GUI()
        self._GUI.setCallbacks(self.callback_VerifyNotas, self.callback_Configuracoes, self.callback_Login)
        self.changeWindow("main")
        
        #Schedule update
        kivy.clock.Clock.schedule_interval(self._callback_update, 0)
        
        #Send configuration to service
        self._callback_configchange('login', self.config.get('account', 'login'))
        self._callback_configchange('password', self.config.get('account', 'password'))
        self._callback_configchange('timeout', self.config.get('account', 'update_time'))
        self._callback_configchange('hash', self.config.get('account', 'lasthash'))
        print "CONFIGURA: "+self.config.get('account', 'update_time')
        
    def on_stop(self):
        self._callback_programexit()
    
    def build_config(self, config):
        config.setdefaults('account', {'login': '','password': '', 'update_time': '60', 'lasthash': '', 'update_auto': '1'})
        kivy.Config.set('kivy', 'exit_on_escape', 0)
        kivy.Config.set('kivy', 'log_enable', 0)
        
        #self.config = config
    
    def build_settings(self, settings):
        jsondata = open('config.json', 'r').read()
        settings.add_json_panel('SigmaWeb+', self.config, data=jsondata)
    
    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            
            if token == ('account', 'login'):
                self._callback_configchange('login', value)
            elif token == ('account', 'password'):
                self._callback_configchange('login', value)
            elif token == ('account', 'update_time'):
                self._callback_configchange('timeout', value)