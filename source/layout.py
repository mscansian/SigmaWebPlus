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

import datetime

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
      
    def setNotas(self, alunoObject):
        if not (self.getWindow() == screenMain):
            return False
        elif alunoObject == None: #Nao ha notas dispoiveis
            return False
        
        pagina = self.window.paineis.index
        self.window.paineis.clear_widgets() #Deleta os paineis antigos
        
        #Cria a home page
        homePanel = SigmaWebHomePage()
        self.window.paineis.add_widget(homePanel)
        homePanel.dados.text = '[b]'+alunoObject.nome+'[/b]\n'+alunoObject.matricula+'\n'+alunoObject.centro
        homePanel.lastupdate.text = "Ultima atualizacao em "+str(datetime.datetime.fromtimestamp(float(alunoObject.time)).strftime('%d/%m/%y %H:%M'))
        homePanel.materias.height = 0 #Hack
        for materia in alunoObject.materias:
            materiaLinha = Materia()
            homePanel.materias.add_widget(materiaLinha)
            homePanel.materias.height = homePanel.materias.height + materiaLinha.height #Hack
            materiaLinha.codigo.text = materia.get("Cod")
            materiaLinha.nota.text = str("%.1f" % materia.get("MediaParcial")) if (materia.get("MediaParcial")<>None) else ("N.Pub")
            
        
        for materia in alunoObject.materias:            
            painel = SigmaWebPage()
            painel.header.text = materia.get("Nome")+'\n[b]'+materia.get("Cod")+'[/b]'
                      
            if len(materia.get("Notas")) > 0:
                painel.notas.clear_widgets()
                painel.notas.height = 0 #Hack
            
            for nota in materia.get("Notas"):
                notaLinha = Nota()
                painel.notas.add_widget(notaLinha)
                painel.notas.height = painel.notas.height + notaLinha.height #Hack
                notaLinha.nome.text = nota.get("Desc")  if (nota.get("Desc")<>None)  else "N.Pub"
                notaLinha.peso.text = str(nota.get("Peso"))+"%"  if (nota.get("Peso")<>None)  else "N.Pub"
                notaLinha.nota.text = str(nota.get("Valor")) if (nota.get("Valor")<>None) else "N.Pub"
            
            if len(materia.get("Notas")) > 0:
                notaLinha = Nota2()
                painel.notas.add_widget(notaLinha)
                painel.notas.height = painel.notas.height + notaLinha.height #Hack
                notaLinha.nome.text = "Media parcial"
                notaLinha.nota.text = str("%.1f" % materia.get("MediaParcial")) if (materia.get("MediaParcial")<>None) else "N.Pub"
                
                notaLinha = Nota()
                painel.notas.add_widget(notaLinha)
                painel.notas.height = painel.notas.height + notaLinha.height #Hack
                notaLinha.nome.text = "Exame"
                notaLinha.peso.text = ""
                notaLinha.nota.text = str(materia.get("Exame")) if (materia.get("Exame")<>None) else ("("+str("%.1f" % materia.get("ExameReq"))+")" if (materia.get("ExameReq")<>None) else "")
        
                notaLinha = Nota2()
                painel.notas.add_widget(notaLinha)
                painel.notas.height = painel.notas.height + notaLinha.height #Hack
                notaLinha.nome.text = "[b]Media final[/b]"
                notaLinha.nota.text = "[b]"+str(materia.get("MediaFinal"))+"[/b]" if (materia.get("MediaFinal")<>None) else ""
        
            #painel.content.text = notas
            self.window.paineis.add_widget(painel)
        
        try:
            self.window.paineis.index = pagina
        except:
            self.window.paineis.index = 0
            
    
class screenLogin(kivy.uix.boxlayout.BoxLayout):
    pass

class screenMain(kivy.uix.boxlayout.BoxLayout):
    pass

class SigmaWebPage(kivy.uix.boxlayout.BoxLayout):
    pass

class SigmaWebHomePage(kivy.uix.boxlayout.BoxLayout):
    pass

class Materia(kivy.uix.boxlayout.BoxLayout):
    pass

class Nota(kivy.uix.boxlayout.BoxLayout):
    pass

class Nota2(kivy.uix.boxlayout.BoxLayout):
    pass