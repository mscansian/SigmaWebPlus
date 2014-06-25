#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
    kivyapp.py
    
    Este arquivo descreve a classe KivyApp que é a classe derivada de kivy.app.App do kivy. Esta classe é necessaria para
    inicializar um aplicativo com o kivy. Após inicializar a classe, voce deve setar uma classe parent (atraves de 
    KivyApp.parent) para receber um callback de todas as funcoes que forem chamadas nesta classe.
    
    Metodos publicos
        (Varios, mas não existe a necessidade de chamar eles)
        
    Dependencias (dentro do projeto)
        
'''

from kivy import Config
from kivy.app import App
from kivy.clock import Clock

class KivyApp(App):
    parent = None
    
    def build(self):
        if self.parent == None: raise KivyAppException("Variable parent not defined in KivyApp")
        Config.set('kivy', 'exit_on_escape', 0)
        Config.set('kivy', 'log_enable', 0)
        Clock.schedule_interval(self.on_update, 0) #Schedule main update
    
    def on_start(self):
        return self.parent.on_start()
    
    def on_stop(self):
        return self.parent.on_stop()
    
    def on_pause(self):
        return self.parent.on_pause()
    
    def on_resume(self):
        return self.parent.on_resume()
    
    def on_update(self, *args):
        return self.parent.on_update()
    
    def build_settings(self, settings):
        self.parent.build_settings(settings)
    
    def build_config(self, config):
        self.parent.build_config(config)
    
    def on_config_change(self, config, section, key, value):
        self.parent.on_config_change(config, section, key, value)
    
    def on_event(self, *args):
        self.parent.on_event(*args)

class KivyAppException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)