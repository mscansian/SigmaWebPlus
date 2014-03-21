#!/usr/bin/python
# -*- coding: UTF-8 -*-

import kivy.app
import kivy.config
import kivy.utils

import layout

class SigmaWebApp(kivy.app.App):
    _SigmaWeb = None
    _Service = None

    #Kivy Configuration
    use_kivy_settings = False

    #Override methods
    def build(self):
        if kivy.utils.platform == 'android':
            import android
            print "servico iniciado dentro"
            service = android.AndroidService('SigmaWeb+', 'Monitorando')
            service.start('')
            self.service = service
              
        self._SigmaWeb = SigmaWeb(self.on_window_change, self.open_settings)
    
    def on_start(self):
        pass
    
    def build_config(self, config):
        config.setdefaults('account', {
                                    'login': '',
                                    'password': ''})
    
    def build_settings(self, settings):
        jsondata = '[{ "type": "title","title": "Atualização Automatica" }]'
        settings.add_json_panel('Configurações',
                                self.config, data=jsondata)
    
    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            
            if token == ('account', 'login'):
                pass
    
    #Custom methods
    def on_window_change(self, window):
        self.root = window

class SigmaWeb():
    _CurrentWindow = None
    _WindowChangeCallback = None
    _OpenSettingsCallback = None
    
    #Specific methods
    def on_configuracoes_press(self, instance):
        self._OpenSettingsCallback()
    
    def on_update_press(self, instance):
        pass
    
    #Common methods
    def __init__(self, winChangeCallback, openSettingsCallback):
        self._WindowChangeCallback = winChangeCallback
        self._OpenSettingsCallback = openSettingsCallback
        self.build()
        
    def build(self):        
        self.changeWindow(layout.MainWindow(self.on_configuracoes_press, self.on_update_press))
    
    def changeWindow(self, window):
        self._CurrentWindow = window
        self._WindowChangeCallback(window.getRoot())
        
    
#Avoid this script to be run as main
if __name__ == '__main__':
    import sys
    sys.exit(1)