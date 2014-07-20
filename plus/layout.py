from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from xmlparser import aluno
from kivy.utils import platform

class GUI:
    root = None
    _properties = None
    _window = None
    
    def __init__(self, kvFile):
        self.root = BoxLayout()
        Builder.load_file(kvFile)
        self._properties = {}
        
    def setWindow(self, window):
        self.root.clear_widgets()
        self._window = window()
        self._window.setProperty(self._properties)
        self.root.add_widget(self._window)
    
    def getWindow(self):
        return self._window.__class__
    
    def setProperty(self, key, value):
        self._properties[key] = value
        if self._window <> None: self._window.setProperty({key:value})
    
    def getProperty(self, key):
        return self._properties[key]

class screenBase():
    def setProperty(self, prop):
        raise NotImplementedError("No implementation of setProperty()")

class screenLogin(BoxLayout, screenBase):
    def setProperty(self, prop):
        for key in prop:
            value = prop[key]
            if key == 'msg_error':
                self.msg_error = value

class screenMain(BoxLayout, screenBase):   
    homePage = None
    text_msg = None
    
    def setProperty(self, prop):
        for key in prop:
            value = prop[key]
            if key == 'userdata':
                self._createView(value)
                self._stopLoading()
            elif key == 'usermsg':
                if self.homePage is not None: 
                    self.text_msg = value
                    self.homePage.text_msg = value
                    self._updateTogge()
                self._stopLoading()
            elif key == 'toggleupdate':
                self._updateTogge()
            elif key == 'update_auto':
                self.service_state = value
    
    def _updateTogge(self):
        if self.homePage is not None:
            self.homePage.text_msg = self.text_msg
            if (self.tog.btn_state == '0'):
                self.homePage.text_msg = self.homePage.text_msg + "\n[color=ff0000]Monitoramento automatico: [b]DESATIVADO[/b][/color]"
            else:
                self.homePage.text_msg = self.homePage.text_msg + "\nMonitoramento automatico: [color=00aa00][b]ATIVADO[/b][/color]"
    
    def _stopLoading(self):
        self.refresh.loading = 0
    
    def _createView(self, xmlData):
        alunoObject = aluno(xmlData) #Cria o objeto do aluno a partir do XML
        try: paginaAtual = self.paginas.current_slide.header
        except: paginaAtual = 'Home'
        
        #Limpa as informacoes antigas
        self.paginas.clear_widgets()
        if (platform == 'android'):
            try: self.page_header.parent.remove_widget(self.page_header)
            except: pass
        else: self.page_header.clear_widgets()
        self.homePage = pageHome()
        self.homePage.text_header = '[b]'+alunoObject.get('Nome')+'[/b]\n'+alunoObject.get('Matricula')+'\n'+alunoObject.get('Centro')
        
        
        self.homePage.materias.height = 0 #Hack
        self.paginas.add_widget(self.homePage)
        for materia in alunoObject.get('Materias'):
            #Adiciona resultados parciais na Home
            homePageMateria = pageHomeMateria()
            if materia['MediaFinal'] is None:
                homePageMateria.codigo = materia['Cod']
                homePageMateria.nota = (str("%.1f" % materia['MediaParcial']) if materia['MediaParcial']!=None else 'N.Pub')
            elif float(materia['MediaParcial']) >= 5.0:
                homePageMateria.codigo = '[color=00aa00]'+materia['Cod']+'[/color]'
                homePageMateria.nota = '[color=00aa00]'+str("%.1f" % materia['MediaParcial'])+'[/color]'
            else:
                homePageMateria.codigo = '[color=ff0000]'+materia['Cod']+'[/color]'
                homePageMateria.nota = '[color=ff0000]'+str("%.1f" % materia['MediaParcial'])+'[/color]' 
            self.homePage.materias.add_widget(homePageMateria)
            self.homePage.materias.height += homePageMateria.height #Hack
            
            #Adiciona botao para desktop
            if platform != 'android': self.page_header.add_widget(screenMainButton(text=materia['Cod']))
            
            #Adiciona pagina com notas da materia
            materiaPage = pageMateria()
            materiaPage.header = '[b]'+materia['Nome']+'[/b]\n'+materia['Cod']+''
            self.paginas.add_widget(materiaPage)
            
            if len(materia['Notas']) > 0:
                materiaPage.notas.height = 0 #Hack
                materiaPage.notas.clear_widgets()
                for nota in materia['Notas']:
                    materiaPageNota = pageMateriaNota()
                    materiaPageNota.codigo = nota['Desc']
                    materiaPageNota.peso = nota['Peso']+'%'
                    materiaPageNota.nota = ((str("%.1f" % nota['Valor']) if isinstance(nota['Valor'],float) else nota['Valor']) if nota['Valor']!=None else 'N.Pub')
                    materiaPage.notas.add_widget(materiaPageNota)
                    materiaPage.notas.height += materiaPageNota.height #Hack
                
                #Media Parcial
                materiaPageNota = pageMateriaNotaFinal()
                materiaPageNota.codigo = 'Media parcial'
                materiaPageNota.nota = ((str("%.1f" % materia['MediaParcial']) if isinstance(materia['MediaParcial'],float) else materia['MediaParcial']) if materia['MediaParcial']!=None else 'N.Pub')
                materiaPage.notas.add_widget(materiaPageNota)
                materiaPage.notas.height += materiaPageNota.height #Hack
                
                #Exame
                materiaPageNota = pageMateriaNota()
                if (materia['Exame'] is not None) or (materia['ExameReq'] is None):
                    materiaPageNota.codigo = 'Exame'
                    materiaPageNota.nota = ((str("%.1f" % materia['Exame']) if isinstance(materia['Exame'],float) else materia['Exame']) if materia['Exame']!=None else 'N.Pub')
                else:
                    materiaPageNota.codigo = 'Exame [necessario]'
                    materiaPageNota.nota = ((str("%.1f" % materia['ExameReq']) if isinstance(materia['ExameReq'],float) else materia['ExameReq']) if materia['ExameReq']!=None else 'N.Pub')
                materiaPage.notas.add_widget(materiaPageNota)
                materiaPage.notas.height += materiaPageNota.height #Hack

                #Media Final
                materiaPageNota = pageMateriaNotaFinal()
                materiaPageNota.codigo = 'Media final'
                materiaPageNota.nota = ((str("%.1f" % materia['MediaFinal']) if isinstance(materia['MediaFinal'],float) else materia['MediaFinal']) if materia['MediaFinal']!=None else 'N.Pub')
                materiaPage.notas.add_widget(materiaPageNota)
                materiaPage.notas.height += materiaPageNota.height #Hack
        
        if self.homePage.materias.height == 0: #Nenhuma materia disponivel
            homePageMateria = Label(text='[color=ff0000]Nenhuma materia disponivel[/color]', markup=True)
            self.homePage.materias.add_widget(homePageMateria)
            self.homePage.materias.height += homePageMateria.font_size * 3 #Hack

class screenLoading(BoxLayout, screenBase):
    def setProperty(self, prop):
        for key in prop:
            value = prop[key]
            if key == 'msg_loading':
                self.msg_loading = value

class screenMainButton(Button):
    pass

class pageHome(BoxLayout):
    pass

class pageHomeMateria(BoxLayout):
    pass

class pageMateria(BoxLayout):
    pass

class pageMateriaNota(BoxLayout):
    pass

class pageMateriaNotaFinal(BoxLayout):
    pass