#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
    main.py
    
    XXX
    
    Metodos publicos
        XXX
        
    Dependencias (dentro do projeto)
        XXX
'''

from kivyapp import KivyApp
from layout import GUI, screenLogin, screenMain, screenLoading
from config import UserConfig
from service import Service, STATE_CONNECTEDTHREAD, STATE_CONNECTEDANDROID, STATE_CONNECTEDREMOTE
from crypto import RSACrypto
from service.version import __version__
from service.debug import Debug
from kivy.utils import platform
from versioncompare import ProgramVersionGreater
if platform=='android': from android_api import AndroidWrapper

class SigmaWeb():
    userConfig = None
    service = None
    kivyApp = None
    GUI = None
    
    def __init__(self):
        #Inicia o app carregando os objetos que vai precisar
        self.GUI = GUI('res/screens.kv')
        self.service = Service()
        self.kivyApp = KivyApp()
        
        #Configura o objeto do kivy e inicia o programa (isso vai chamar o on_start())
        self.kivyApp.root = self.GUI.root
        self.kivyApp.use_kivy_settings = False
        self.kivyApp.parent = self
        self.kivyApp.run()
    
    '''
    ''   KIVY CALLBACKS
    '''
    
    def on_start(self):   
        if ProgramVersionGreater(__version__, self.userConfig.getConfig('app_version')): 
            Debug().warn("Deletando configuracoes de versao antiga!")
            self.userConfig.clearConfig()
        self.userConfig.setConfig('app_delete', '0')
           
        if self.userConfig.getConfig('username') == '':
            self.GUI.setWindow(screenLogin)
        else:
            self.service.start(self.userConfig.exportConfig(), (self.userConfig.getConfig('update_auto')=='0'))
            self.GUI.setWindow(screenLoading)
    
    def on_stop(self):
        self.userConfig.write()
        self.service.stop(((self.userConfig.getConfig('update_auto')=='0') or (self.userConfig.getConfig('app_delete')=='1')))
        Debug().note("Aplicativo foi finalizado com sucesso!")
    
    def on_pause(self):
        if self.userConfig.getConfig('debug_disablepause')=='0': 
            self.userConfig.write()
            self.service.stop((self.userConfig.getConfig('update_auto')=='0'))
            Debug().note("Aplicativo foi pausado com sucesso!")
            return True
        else: return False
    
    def on_resume(self):
        self.on_start()
    
    def on_update(self, *args):
        keys = self.service.getKeys()
        if keys <> None:
            for keypair in keys:
                key, value = keypair
                self.userConfig.setConfig(key, value)
                if key == 'update_msg':
                    self.GUI.setProperty('userdata', [self.userConfig.getConfig('update_data'), value])
                elif key == 'update_data':
                    self.GUI.setProperty('userdata', [value, self.userConfig.getConfig('update_msg')])
                elif key == 'update_auto':
                    self.GUI.setProperty('update_auto', value)
                elif key == 'username':
                    if value == '':
                        self.service.stop()
                        self.GUI.setProperty('msg_error', 'Login ou senha incorreto')
                        self.GUI.setWindow(screenLogin)
                    
        
        if self.GUI.getWindow() <> screenMain:
            if self.userConfig.getConfig('update_data') <> '':
                self.GUI.setProperty('userdata', [self.userConfig.getConfig('update_data'), self.userConfig.getConfig('update_msg')])
                self.GUI.setProperty('update_auto', self.userConfig.getConfig('update_auto'))
                self.GUI.setWindow(screenMain)
    
    def build_settings(self, settings):
        jsonConfig = open('res/config.json', 'r').read()
        jsonConfigDebug = open('res/config_debug.json', 'r').read()
        settings.add_json_panel('Configuracoes', self.userConfig.kivyConfig, data=jsonConfig)
        settings.add_json_panel('Debug', self.userConfig.kivyConfig, data=jsonConfigDebug)
    
    def build_config(self, config):        
        defaultSection = 'Sigmauser'
        defaultConfig = {
                         'username'           : '',
                         'password'           : '', 
                         'update_timeout'     : '180', 
                         'update_time'        : '0', 
                         'update_hash'        : '', 
                         'update_auto'        : '0',
                         'update_force'       : '0', 
                         'update_data'        : '', 
                         'update_msg'         : '',
                         'app_version'        : __version__,
                         'app_delete'         : '0',
                         'debug_disablepause' : '1',
                         'debug_toast'        : '0'
                         }
        
        self.userConfig = UserConfig(config, defaultSection, defaultConfig)
        
    def on_config_change(self, config, section, key, value):
        self.service.setKey(key, value)
        if key == 'app_delete':
            self.userConfig.setConfig('username', '')
            self.userConfig.setConfig('password', '')
            self.userConfig.setConfig('update_time', '0')
            self.userConfig.setConfig('update_hash', '')
            self.userConfig.setConfig('update_data', '')
            self.userConfig.setConfig('update_msg', '')
            self.kivyApp.stop()
    
    def on_event(self, *args):
        type = args[0]
        if type == 'Login':
            type, username, password = args
            if (username=='') or (password==''): self.GUI.setProperty("msg_error", "Preenchas seus dados")
            else:
                self.userConfig.setConfig('username', username)
                self.userConfig.setConfig('password', RSACrypto('res/sigmawebplus-server.pub').encrypt(password))
                self.userConfig.setConfig('update_time', '0')
                self.userConfig.setConfig('update_hash', '')
                self.userConfig.setConfig('update_data', '')
                self.userConfig.setConfig('update_msg', '')
                self.service.start(self.userConfig.exportConfig(), (self.userConfig.getConfig('update_auto')=='0'))
                self.GUI.setWindow(screenLoading)
                self.GUI.setProperty("msg_loading", "[b]Aguarde[/b]\n\nRealizando login...")
        elif type == 'Reload':
            if self.service.getKey('update_force') == '0': self.service.setKey('update_force', '1')
        elif type == 'SwitchPanel':
            pass
        elif type == 'ServiceToggle':
            type, value = args
            self.userConfig.setConfig('update_auto', str(value)) #Atualiza arquivo de config
            self.service.setKey('update_auto', str(value))       #Atualiza service
            if self.service.isAlive() and (platform == 'android'):
                if (value == '0') and ((self.service.getState() == STATE_CONNECTEDREMOTE) or (self.service.getState() == STATE_CONNECTEDANDROID)):
                    self.service.stop()
                    self.service.start(self.userConfig.exportConfig(), True)
                    if (platform=='android') and (self.userConfig.getConfig('debug_toast')=='1'): AndroidWrapper().Toast('Monitor de notas desativado')
                elif (value == '1') and (self.service.getState() == STATE_CONNECTEDTHREAD):
                    self.service.stop()
                    self.service.start(self.userConfig.exportConfig())
                    if (platform=='android') and (self.userConfig.getConfig('debug_toast')=='1'): AndroidWrapper().Toast('Monitor de notas ativado')
        
if __name__ == '__main__':
    SigmaWeb()