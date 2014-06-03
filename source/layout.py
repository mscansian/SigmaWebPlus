#!/usr/bin/python
# -*- coding: UTF-8 -*-

import kivy.uix.image
import kivy.uix.boxlayout
import kivy.uix.anchorlayout
import kivy.uix.button
import kivy.uix.tabbedpanel
import kivy.uix.label
import kivy.uix.textinput
import kivy.utils


class GUI():
    _currentWindow = None
    
    #Callbacks
    _callback_VerifyNotas = None
    _callback_Configuracoes = None
    _callback_Login = None
    
    #GUI variables
    def getLoginMatricula(self):
        try:
            return self._currentWindow._LoginMatricula.text
        except:
            return ""
        
    def getLoginSenha(self):
        try:
            return self._currentWindow._LoginSenha.text
        except:
            return ""
    
    def setCallbacks(self, VerifyNotas, Configuracoes, Login):
        self._callback_VerifyNotas = VerifyNotas
        self._callback_Configuracoes = Configuracoes
        self._callback_Login = Login
    
    def change(self, window):
        if window == "login":
            print "login win"
            self._currentWindow = LoginWindow(self._callback_Login)
        elif window == "main":
            print "main win"
            self._currentWindow = MainWindow(self._callback_Configuracoes, self._callback_VerifyNotas)
        else:
            raise
    
    def getRoot(self):
        return self._currentWindow.getRoot()             

class BaseWindow():
    _Root = None
    
    def getRoot(self):
        return self._Root

class MainWindow(BaseWindow):
    _Logo = None
    _Tabs = None
    _Buttons = None
    
    
    def __init__(self, configcallback, updatecallback):
        self._Root = kivy.uix.boxlayout.BoxLayout()
        self._Root.orientation = 'vertical'
         
        self._Logo = kivy.uix.image.Image()
        self._Logo.source = 'res/logo.png'
        self._Logo.size_hint = (1, 0.3)
        self._Root.add_widget(self._Logo)
        
        self._Tabs = kivy.uix.tabbedpanel.TabbedPanel()
        self._Tabs.do_default_tab = True
        self._Tabs.default_tab_text = 'Início'
        self._Root.add_widget(self._Tabs)
        
        self._Buttons = kivy.uix.boxlayout.BoxLayout()
        self._Buttons.size_hint = (1, 0.1)
        self._Root.add_widget(self._Buttons)
        
        #Configuration button is not necessary on android devices
        if kivy.utils.Platform() <> "android":
            self._ButtonConfig = kivy.uix.button.Button()
            self._ButtonConfig.text = 'Configurações'
            self._ButtonConfig.bind(on_press=configcallback)
            self._Buttons.add_widget(self._ButtonConfig)
        
        self._ButtonUpdate = kivy.uix.button.Button()
        self._ButtonUpdate.text = 'Verificar notas'
        self._ButtonUpdate.bind(on_press=updatecallback)
        self._Buttons.add_widget(self._ButtonUpdate)
    
class LoginWindow(BaseWindow):
    _Logo = None
    _LoginBox = None
    
    def __init__(self, logincallback):
        self._Root = kivy.uix.boxlayout.BoxLayout()
        self._Root.orientation = 'vertical'
        
        self._Logo = kivy.uix.image.Image()
        self._Logo.source = 'res/logo.png'
        self._Logo.size_hint = (1, 0.3)
        self._Root.add_widget(self._Logo)
        
        self._LoginBox = kivy.uix.boxlayout.BoxLayout()
        self._LoginBox.orientation = 'vertical'
        self._LoginBox.size_hint = (1, 0.5)
        self._Root.add_widget(self._LoginBox)
        
        self._LoginMatriculaBox = kivy.uix.boxlayout.BoxLayout()
        self._LoginBox.add_widget(self._LoginMatriculaBox)
        
        self._LoginMatriculaLabel = kivy.uix.label.Label(text="Matricula", size_hint=(0.3,1))
        self._LoginMatriculaBox.add_widget(self._LoginMatriculaLabel)
        
        self._LoginMatricula = kivy.uix.textinput.TextInput()
        self._LoginMatricula.multiline = False
        self._LoginMatriculaBox.add_widget(self._LoginMatricula)
        
        self._LoginSenhaBox = kivy.uix.boxlayout.BoxLayout()
        self._LoginBox.add_widget(self._LoginSenhaBox)
        
        self._LoginSenhaLabel = kivy.uix.label.Label(text="Senha", size_hint=(0.3,1))
        self._LoginSenhaBox.add_widget(self._LoginSenhaLabel)
        
        self._LoginSenha = kivy.uix.textinput.TextInput()
        self._LoginSenha.password = True
        self._LoginSenha.multiline = False
        self._LoginSenhaBox.add_widget(self._LoginSenha)
        
        self._LoginButton = kivy.uix.button.Button()
        self._LoginButton.text = 'Entrar'
        self._LoginButton.bind(on_press=logincallback)
        self._LoginBox.add_widget(self._LoginButton)