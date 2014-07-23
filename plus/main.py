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
from threading import Thread

from kivy.utils import platform

from kivyapp import KivyApp
from layout import GUI, screenLogin, screenMain, screenLoading
from config import UserConfig
from service import Service, STATE_CONNECTEDTHREAD, STATE_CONNECTEDANDROID, STATE_CONNECTEDREMOTE, STATE_NOTSTARTED
from crypto import RSACrypto
from service.version import __version__
from service.debug import Debug
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
    
    '''
    Chamada no momento que o usuario abre o app
    '''
    def on_start(self):
        Debug().note("on_start()")
        '''
        Faz algumas correcoes no arquivo de configuracao se a versao anterior era mais antiga que a atual
        '''
        if ProgramVersionGreater(__version__, self.userConfig.getConfig('app_version')): 
            Debug().warn("Deletando configuracoes de versao antiga!")
            username = self.userConfig.getConfig('username')
            password = self.userConfig.getConfig('password')
            self.userConfig.clearConfig()
            self.userConfig.setConfig('username', username)
            self.userConfig.setConfig('password', password)
            if self.userConfig.getConfig('username') != '': self.userConfig.setConfig('update_login', '1')
        self.userConfig.setConfig('app_delete', '0')
        
        '''
        Verifica se o usuario ja realizou o login
        '''
        if self.userConfig.getConfig('username') == '':
            self._clearConfig()
            self.GUI.setWindow(screenLogin)
        else:
            if self.userConfig.getConfig('update_login') == '0':
                self.service.start(self.userConfig.exportConfig(), (self.userConfig.getConfig('update_auto')=='0'))
                self.GUI.setProperty("msg_loading", "Carregando notas... Aguarde!")
            else:
                self.service.start(self.userConfig.exportConfig(), False)
                self.GUI.setProperty("msg_loading", "[b]Buscando notas no sistema[/b]\n\nDependendo da carga no servidor\nisto pode demorar")
            if self.GUI.getWindow() == 'NoneType': self.GUI.setWindow(screenLoading)
    
    def on_stop(self):
        Debug().note("on_stop()")
        self.userConfig.write()
        if (self.userConfig.getConfig('debug_forceexit')=='1'): Debug().warn("debug_forceexit = 1")
        self.service.stop(((self.userConfig.getConfig('update_auto')=='0') or (self.userConfig.getConfig('app_delete')=='1') or (self.userConfig.getConfig('debug_forceexit')=='1')))
        Debug().note("Aplicativo foi finalizado com sucesso!")
    
    def on_pause(self):
        Debug().note("on_pause()")
        if self.userConfig.getConfig('debug_disablepause')=='0':
            self.userConfig.write()
            self.service.stop((self.userConfig.getConfig('update_auto')=='0' and self.userConfig.getConfig('update_login') == '0'))
            Debug().note("Aplicativo foi pausado com sucesso!")
            return True
        else: return False
    
    def on_resume(self):
        Debug().note("on_resume()")
        self.on_start()
    
    def on_update(self, *args):
        keys = self.service.getKeys()
        if keys is not None:
            for keypair in keys:
                key, value = keypair
                self.userConfig.setConfig(key, value)
                
                '''
                Mensagens que o service manda para avisa o usuario de algum acontecimento
                '''
                if key == 'update_msg':
                    '''
                    Erro no servidor (durante login). Faz logoff do usuario e mostra uma mensagem na tela de login
                    '''
                    if (self.userConfig.getConfig('update_login') == '1') and (value[:46] == '[color=ff0000][b]Erro no servidor![/b][/color]'):
                        self.service.stop()
                        self._clearConfig()
                        self.GUI.setProperty('msg_error', 'Erro ao acessar o sistema. \nTente novamente mais tarde')
                        self.GUI.setWindow(screenLogin)
                    else:
                        #Mensagem nao eh um erro entao mostra ela com a cor normal
                        self.GUI.setProperty('usermsg', value)
                
                #Dados que o service baixou do usuario
                elif (key == 'update_data'):
                    self.GUI.setProperty('userdata', value)
                    
                    if (platform == 'android') and (self.GUI.getWindow() is not screenMain) and (self.userConfig.getConfig('update_login') == '1'): #Reinicia o server caso seja android (Muda a mensagem de login)
                        self.userConfig.setConfig('update_login', '0')
                        if self.userConfig.getConfig('update_auto')=='0':
                            Debug().error("Reinicializando service...")
                            self.service.start(self.userConfig.exportConfig(), True)
                elif key == 'update_auto':
                    self.GUI.setProperty('update_auto', value)
                elif key == 'username':
                    if value == '':
                        self._clearConfig()
                        self.service.stop()
                        self.GUI.setProperty('msg_error', 'Login ou senha incorreto')
                        self.GUI.setWindow(screenLogin)
                elif key == 'app_delete':
                    Debug().error("Iniciando o procedimento do app_delete...")
                    self._clearConfig()
                    self.kivyApp.stop()
                    
        
        if self.GUI.getWindow() is not screenMain:
            if (self.userConfig.getConfig('update_data') != '') and (self.userConfig.getConfig('username') != ''):
                self.GUI.setProperty('userdata', self.userConfig.getConfig('update_data'))
                self.GUI.setWindow(screenMain)
                self.GUI.setProperty('update_auto', self.userConfig.getConfig('update_auto')) #Seta o estado inicial do botao
                self.GUI.setProperty('usermsg', self.userConfig.getConfig('update_msg'))
    
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
                         'update_auto'        : '1',
                         'update_force'       : '0', 
                         'update_data'        : '', 
                         'update_msg'         : '',
                         'update_login'       : '0',
                         'app_version'        : __version__,
                         'app_delete'         : '0',
                         'debug_disablepause' : '0',
                         'debug_toast'        : '0',
                         'debug_serverout'    : '0',
                         'debug_forceexit'    : '0',
                         'debug_errortimeout' : '10'
                         }
        
        self.userConfig = UserConfig(config, defaultSection, defaultConfig)
        
    def on_config_change(self, config, section, key, value):
        self.service.setKey(key, value)
        if key == 'app_delete':
            Debug().error("Iniciando o procedimento do app_delete...")
            self._clearConfig()
            self.kivyApp.stop()
        elif key == 'update_timeout':
            if int(value) < 30:
                self.userConfig.setConfig('update_timeout', '30')
        elif key == 'update_auto':
            if (self._toggleService(value)): self.GUI.setProperty('update_auto', value)
    
    def on_event(self, *args):
        type = args[0]
        if type == 'Login':
            type, username, password = args
            if (username=='') or (password==''): self.GUI.setProperty("msg_error", "Preenchas seus dados")
            else:
                self._clearConfig()
                self.userConfig.setConfig('username', username)
                self.userConfig.setConfig('password', RSACrypto('res/sigmawebplus-server.pub').encrypt(password))
                self.userConfig.setConfig('update_login', '1')
                self.service.start(self.userConfig.exportConfig(), False)
                self.GUI.setWindow(screenLoading)
                self.GUI.setProperty("msg_loading", "[b]Buscando notas no sistema[/b]\n\nDependendo da carga no servidor\nisto pode demorar")
        elif type == 'Reload':
            if self.service.getKey('update_force') == '0': self.service.setKey('update_force', '1')
        elif type == 'SwitchPanel':
            pass
        elif type == 'ServiceToggle':
            type, value = args
            return self._toggleService(value)
    
    def _toggleService(self, value):
        if (platform == 'android') and (not self.service.isAlive()): return False
        self.userConfig.setConfig('update_auto', str(value)) #Atualiza arquivo de config
        self.service.setKey('update_auto', str(value))       #Atualiza service
        self.GUI.setProperty('toggleupdate', str(value))
        if self.service.isAlive() and (platform == 'android'):
            if (value == '0') and ((self.service.getState() == STATE_CONNECTEDREMOTE) or (self.service.getState() == STATE_CONNECTEDANDROID)):
                self.service.start(self.userConfig.exportConfig(), True)
                if (platform=='android') and (self.userConfig.getConfig('debug_toast')=='1'): AndroidWrapper().Toast('Monitor de notas desativado')
            elif (value == '1') and (self.service.getState() == STATE_CONNECTEDTHREAD):
                self.service.start(self.userConfig.exportConfig())
                if (platform=='android') and (self.userConfig.getConfig('debug_toast')=='1'): AndroidWrapper().Toast('Monitor de notas ativado')
        return True
    
    def _clearConfig(self):
        self.userConfig.setConfig('username', '')
        self.userConfig.setConfig('password', '')
        self.userConfig.setConfig('update_time', '0')
        self.userConfig.setConfig('update_hash', '')
        self.userConfig.setConfig('update_data', '')
        self.userConfig.setConfig('update_msg', '')
        self.userConfig.setConfig('update_login', '0')         
        
if __name__ == '__main__':
    SigmaWeb()