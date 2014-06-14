#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import kivy.app
import kivy.config
import kivy.utils
import kivy.clock

import serverXMLparser
import layout

class KivyApp(kivy.app.App):
    GUI = None
    
    #Private variables
    _callback_update = None
    _callback_event = None
    
    
    #Kivy Configuration
    use_kivy_settings = False
    
    def setCallback(self, update, event):
        self._callback_update = update
        self._callback_event = event
    
    def updateNotas(self, hash, notas, home):     
        if notas == "":
            hash = self.config.get('account', 'lasthash')
            notas = self.config.get('account', 'notas_data')
        
        if not (notas==""):
            #Salva hash e notas
            self.config.set('account', 'lasthash', hash)
            self.config.set('account', 'notas_data', notas)
            self.config.write()
            
            dadosAluno = serverXMLparser.alunoXML(notas) #Faz um parse do codigo XML para mostrar as notas
            self.GUI.setNotas(dadosAluno.materias, home) #Modifica pagina mostrando as notas
        
    #Override methods
    def build(self):
        #Load GUI
        self.GUI = layout.GUI()
        self.root = self.GUI.root
        
        kivy.clock.Clock.schedule_interval(self._callback_update, 0) #Schedule main update
         
    def on_start(self):
        #Hack: Seta o valor da configracao de deletar dados para False
        self.config.set('account', 'delall', '0')
        self.config.write()
        
        self.GUI.setWindow(layout.screenLogin) #Carrega janela de login
        self.on_event("Login", self.config.get('account', 'login'), self.config.get('account', 'password')) #Tenta realizar o login
        self.updateNotas(self.config.get('account', 'lasthash'), self.config.get('account', 'notas_data'), "Suas notas estao sendo atualizadas\nAguarde...") #Carrega notas salvas
                
        self.on_event("ProgramStart", self.config.get('account', 'lasthash'), self.config.get('account', 'update_time'), self.config.get('account', 'update_auto'))
        
    def on_stop(self):
        self.on_event("ProgramExit")
        
    def on_pause(self):
        if self.GUI.getWindow() == layout.screenLogin: #If app is on Login screen, then closes everything
            return False
        else:
            return True
    
    def on_resume(self):
        pass
    
    def build_config(self, config):
        config.setdefaults('account', {'login': '','password': '', 'update_time': '60', 'lasthash': '', 'update_auto': '1', 'notas_data': '', 'delall': '0'})
        kivy.Config.set('kivy', 'exit_on_escape', 0)
        kivy.Config.set('kivy', 'log_enable', 0)
    
    def build_settings(self, settings):
        jsondata = open('config.json', 'r').read()
        settings.add_json_panel('SigmaWeb+', self.config, data=jsondata)
    
    def on_config_change(self, config, section, key, value):
        self.on_event("ConfigChange", config, section, key, value) #Forward to event handler
                
    def on_event(self, eventType, *args):
        #Deal with the event locally
        if eventType == "VerificarNotas":
            self.updateNotas(self.config.get('account', 'lasthash'), self.config.get('account', 'notas_data'), "Suas notas estao sendo atualizadas\nAguarde...") #Atualiza home
        elif eventType == "Login":
            matricula = args[0]
            senha = args[1]
            
            if not ((matricula == "") or (senha=="")):
                self.config.set('account', 'login', matricula)
                self.config.set('account', 'password', senha)
                self.config.write()
                
                self.GUI.setWindow(layout.screenMain)
        elif eventType == "Logoff":
            self.config.set('account', 'login', '')
            self.config.set('account', 'password', '')
            self.config.set('account', 'lasthash', '')
            self.config.set('account', 'notas_data', '')
            self.config.write()
            
            self.GUI.setWindow(layout.screenLogin)
        elif eventType == "ConfigChange":
            key = args[2]
            if key == 'delall':
                self.config.set('account', 'login', '')
                self.config.set('account', 'password', '')
                self.config.set('account', 'lasthash', '')
                self.config.set('account', 'notas_data', '')
                self.config.write()
                self.stop()
        elif eventType == "ProgramExit":
            pass
        else:
            print "Warning: Event caught but not recognized '"+eventType+"' in kivyapp.py"
        
        self._callback_event(eventType, *args) #Forward event to the main class