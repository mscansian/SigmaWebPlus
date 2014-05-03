#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import kivy.app
import kivy.config
import kivy.utils

import layout
from service.debug import Debug

class SigmaWebApp(kivy.app.App):
    _SigmaWeb = None
    _Service = None
    ThreadComm = None
    
    #Kivy Configuration
    use_kivy_settings = False

    #Override methods
    def build(self):  
        #Start threadcomm
        try:
            import service.threadcomm
            self.ThreadComm = service.threadcomm.ThreadComm(51352, "sigmawebplus")
        except service.threadcomm.ThreadCommException as e:
            sys.exit(e.value)
        
        self._SigmaWeb = SigmaWeb(self.ThreadComm, self.on_window_change, self.open_settings)
    
    def on_start(self):
        pass
    
    def on_stop(self):
        self.ThreadComm.kill()
    
    def build_config(self, config):
        config.setdefaults('account', {
                                    'login': '',
                                    'password': ''})
        kivy.Config.set('kivy', 'exit_on_escape', 0)
        kivy.Config.set('kivy', 'log_enable', 0)
    
    def build_settings(self, settings):
        jsondata = '[{ "type": "title","title": "Atualização Automatica" }]'
        settings.add_json_panel('Configurações',
                                self.config, data=jsondata)
    
    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            
            if token == ('account', 'login'):
                self.ThreadComm.sendMsg("UNC "+value)
            elif token == ('account', 'password'):
                self.ThreadComm.sendMsg("UNP "+value)
    
    #Custom methods
    def on_window_change(self, window):
        self.root = window

class SigmaWeb():
    _CurrentWindow = None
    _WindowChangeCallback = None
    _OpenSettingsCallback = None
    ThreadComm = None
    
    #Specific methods
    def on_configuracoes_press(self, instance):
        self._OpenSettingsCallback()
    
    def on_update_press(self, instance):
        self.ThreadComm.sendMsg("CKN")
    
    #Common methods
    def __init__(self, ThreadComm, winChangeCallback, openSettingsCallback):
        self._WindowChangeCallback = winChangeCallback
        self._OpenSettingsCallback = openSettingsCallback
        self.ThreadComm = ThreadComm
        self.build()
        
    def build(self):
        self.changeWindow(layout.MainWindow(self.on_configuracoes_press, self.on_update_press))
    
    def changeWindow(self, window):
        self._CurrentWindow = window
        self._WindowChangeCallback(window.getRoot())