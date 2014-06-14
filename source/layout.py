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
    root = None
    window = None
    
    def __init__(self):
        self.root = kivy.uix.boxlayout.BoxLayout() #Create root widget
        Builder.load_file('layout.kv') #Load kv file

    def setWindow(self, window):
        self.root.clear_widgets() #Clear current window
        self.window = window() #Save window class
        self.root.add_widget(self.window) #Create object and add to root
    
    def getWindow(self):
        return self.window.__class__
    
    def setNotas(self, notas, home):
        if not (self.getWindow() == screenMain):
            return False
        
        self.window.paineis.clear_widgets() #Deleta os paineis antigos
        
        #Adiciona novamente a Home
        homePanel = SigmaWebPage()
        homePanel.content.text = home
        self.window.paineis.add_widget(homePanel)
        
        for materia in notas:
            painel = SigmaWebPage()
            painel.header.text = materia.get("Cod")+'\n'+materia.get("Nome")
                      
            notas = ''
            for nota in materia.get("Notas"):
                notaValor = nota.get("Valor")
                if notaValor == None:
                    notaValor = "--"
                
                notas = notas + nota.get("Desc")+" ("+nota.get("Peso")+"): "+notaValor + '\n'
        
            painel.content.text = notas
            self.window.paineis.add_widget(painel)
            
    
class screenLogin(kivy.uix.boxlayout.BoxLayout):
    pass

class screenMain(kivy.uix.boxlayout.BoxLayout):
    pass

class SigmaWebPage(kivy.uix.boxlayout.BoxLayout):
    pass