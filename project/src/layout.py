#!/usr/bin/python
# -*- coding: UTF-8 -*-

import kivy.uix.image
import kivy.uix.boxlayout
import kivy.uix.anchorlayout
import kivy.uix.button
import kivy.uix.tabbedpanel
import kivy.uix.label
import kivy.utils

from eventhandler import EventHandler

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
    
    def createObject(self):
        self._Root = kivy.uix.boxlayout.BoxLayout()
        self._Root.orientation = 'vertical'
        
        self._Logo = kivy.uix.image.Image()
        self._Logo.source = 'res/logo.png'
        self._Logo.size_hint = (1, 0.3)
        self._Root.add_widget(self._Logo)
        
        self._LoginBox = kivy.uix.anchorlayout.AnchorLayout()
        self._LoginBox.anchors = ('center', 'center')
        self._Root.add_widget(self._LoginBox)