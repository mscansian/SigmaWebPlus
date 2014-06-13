#!/usr/bin/python
# -*- coding: UTF-8 -*-

from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import ListProperty

import kivy.uix.image
import kivy.uix.boxlayout
import kivy.uix.anchorlayout
import kivy.uix.button
import kivy.uix.carousel
import kivy.uix.label
import kivy.uix.textinput
import kivy.uix.listview
import kivy.utils

import kivy.core.window

class GUI():
    windowname = None
    _currentWindow = None
    
    #Callbacks
    _callback_VerifyNotas = None
    _callback_Configuracoes = None
    _callback_Login = None
    
    def __init__(self):
        #kivy.core.window.Window.clearcolor = (246/255.0,246/255.0,246/255.0, 1)
        kivy.core.window.Window.clearcolor = (0,0,0,1)
        
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
        self.windowname = window
        if window == "login":
            self._currentWindow = LoginWindow(self._callback_Login)
        elif window == "main":
            self._currentWindow = MainWindow(self._callback_Configuracoes, self._callback_VerifyNotas)
        else:
            raise
    
    def setNotas(self, notas):
        self._currentWindow.setNotas(notas)
    
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
        Builder.load_file('layout.kv')
        
        self._Root = kivy.uix.boxlayout.BoxLayout()
        self._Root.orientation = 'vertical'
         
        self._Logo = Logo()
        self._Logo.source = 'res/logo.png'
        self._Logo.size_hint = (1, 0.3)
        #self._Logo.allow_stretch = True
        self._Root.add_widget(self._Logo)
        
        self._Tabs = kivy.uix.carousel.Carousel(direction='right')
        self._Root.add_widget(self._Tabs)
        
        self._TabsHolder = kivy.uix.boxlayout.BoxLayout(orientation='vertical')
        self._Tabs.add_widget(self._TabsHolder)
        
        self._Tip = kivy.uix.label.Label(text='Deslize para a esquerda para ver as notas')
        self._TabsHolder.add_widget(self._Tip)
        
        self._Buttons = kivy.uix.boxlayout.BoxLayout()
        self._Buttons.size_hint = (1, 0.1)
        self._Root.add_widget(self._Buttons)
        
        #Configuration button is not necessary on android devices
        if kivy.utils.Platform() <> "android":
            self._ButtonConfig = Button()
            self._ButtonConfig.text = 'Configurações'
            self._ButtonConfig.bind(on_press=configcallback)
            self._Buttons.add_widget(self._ButtonConfig)
        
        self._ButtonUpdate = Button()
        self._ButtonUpdate.text = 'Verificar notas'
        self._ButtonUpdate.bind(on_press=updatecallback)
        self._Buttons.add_widget(self._ButtonUpdate)
    
    def setNotas(self, notas):
        #Deleta os paineis antigos
        self._Tabs.clear_widgets()
        
        #Adiciona novamente a Home
        self._Tabs.add_widget(self._TabsHolder)
        
        for materia in notas:
            TabsHolder = kivy.uix.boxlayout.BoxLayout(orientation='vertical')
            self._Tabs.add_widget(TabsHolder)
            
            TabsHeader = TabHeader(text=materia.get("Cod")+'\n'+materia.get("Nome"), size_hint=(1,0.2))
            TabsHolder.add_widget(TabsHeader)
            
                      
            notas_list = ''
            for nota in materia.get("Notas"):
                nota_valor = nota.get("Valor")
                if nota_valor == None:
                    nota_valor = "--"
                
                notas_list = notas_list + nota.get("Desc")+" ("+nota.get("Peso")+"): "+nota_valor + '\n'
            
            lista = kivy.uix.label.Label(text=notas_list)
            TabsHolder.add_widget(lista)

            
    
class LoginWindow(BaseWindow):
    _Logo = None
    _LoginBox = None
    
    def __init__(self, logincallback):
        Builder.load_file('layout.kv')
        
        self._Root = kivy.uix.boxlayout.BoxLayout()
        self._Root.orientation = 'vertical'
        
        self._Logo = Logo()
        self._Logo.source = 'res/logo.png'
        self._Logo.size_hint = (1, 0.3)
        self._Root.add_widget(self._Logo)
        
        self._LoginBox = kivy.uix.boxlayout.BoxLayout()
        self._LoginBox.orientation = 'vertical'
        self._LoginBox.size_hint = (1, 0.5)
        self._Root.add_widget(self._LoginBox)
        
        self._LoginMatricula = kivy.uix.textinput.TextInput()
        self._LoginMatricula.multiline = False
        self._LoginMatricula.hint_text='Matricula'
        self._LoginMatricula.input_type='number'

        Box = kivy.uix.boxlayout.BoxLayout(size_hint=(1,0.1))
        Box.add_widget(kivy.uix.label.Label(text='', size_hint=(0.1,1)))
        Box.add_widget(self._LoginMatricula)
        Box.add_widget(kivy.uix.label.Label(text='', size_hint=(0.1,1)))
        self._LoginBox.add_widget(Box)
        
        self._LoginSenha = kivy.uix.textinput.TextInput()
        self._LoginSenha.password = True
        self._LoginSenha.multiline = False
        self._LoginSenha.hint_text='Senha'

        Box = kivy.uix.boxlayout.BoxLayout(size_hint=(1,0.1))
        Box.add_widget(kivy.uix.label.Label(text='', size_hint=(0.1,1)))
        Box.add_widget(self._LoginSenha)
        Box.add_widget(kivy.uix.label.Label(text='', size_hint=(0.1,1)))
        self._LoginBox.add_widget(Box)
        
        self._LoginButton = kivy.uix.button.Button()
        self._LoginButton.text = 'Entrar'
        self._LoginButton.bind(on_press=logincallback)
        Box = kivy.uix.boxlayout.BoxLayout(size_hint=(1,0.1))
        Box.add_widget(kivy.uix.label.Label(text='', size_hint=(0.1,1)))
        Box.add_widget(self._LoginButton)
        Box.add_widget(kivy.uix.label.Label(text='', size_hint=(0.1,1)))
        self._LoginBox.add_widget(Box)
        
        
        self._LoginBox.add_widget(kivy.uix.label.Label(text=''))

class TabHeader(kivy.uix.button.Button):
    pass

class Logo(kivy.uix.image.Image):
    pass

class Button(kivy.uix.button.Button):
    pass