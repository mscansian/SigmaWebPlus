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

    #Kivy Configuration
    use_kivy_settings = False

    #Override methods
    def build(self):    
        self._SigmaWeb = SigmaWeb(self.on_window_change, self.open_settings)
    
    def on_start(self):
        pass
    
    def build_config(self, config):
        config.setdefaults('account', {
                                    'login': '',
                                    'password': ''})
        #kivy.config.set('kivy', 'exit_on_escape', 0)
    
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


class MonitorFacade():
    _Monitor = None
    
    def __init__(self):
        if kivy.utils.platform == 'android':
            import android
            self._Monitor = android.AndroidService('SigmaWeb+', 'Monitorando')
        else:
            import service.main
            self._Monitor = service.main.Monitor()

    def start(self, parametro):
        self._Monitor.start(parametro)
    
    def kill(self):
        if kivy.utils.platform == 'android':
            self._Monitor.stop()
        else:
            self._Monitor.kill()
    
#Program entry point
if __name__ == '__main__':
    #Set up service
    Debug().log("Tentando iniciar monitor...")
    monitor = MonitorFacade()
    monitor.start('parametro')
    
    while True:
        SigmaWebApp().run()
        if kivy.utils.platform == 'android':
            #In android platform is safe to leave (the system will keep the service running)
            break
        else:
            #We should ensure that the service is still running
            break #Todo
    
    Debug().log("Exiting the main program...")
    monitor.kill() #Kill thread
    sys.exit(0)