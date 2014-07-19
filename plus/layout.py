from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
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
        if self._window <> None: self._window.setProperty(self._properties)
    
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
    last_userdata = None
    
    def setProperty(self, prop):
        for key in prop:
            value = prop[key]
            if key == 'userdata':
                self._createView(*value)
                self.last_userdata = value
            elif key == 'update_auto':
                self.service_state = value
                if self.last_userdata is not None: self._createView(*self.last_userdata) #Hack: A maneira que encontrei para mudar a msg de ativado/desativado
    
    def _createView(self, xmlData, text_msg):
        alunoObject = aluno(xmlData) #Cria o objeto do aluno a partir do XML
        try: paginaAtual = self.paginas.current_slide.header
        except: paginaAtual = 'Home'
        
        self.refresh.loading = 0
        
        #Limpa as informacoes antigas
        self.paginas.clear_widgets()
        if (platform == 'android'):
            try: self.page_header.parent.remove_widget(self.page_header)
            except: pass
        else: self.page_header.clear_widgets()
        
        homePage = pageHome()
        homePage.text_header = '[b]'+alunoObject.get('Nome')+'[/b]\n'+alunoObject.get('Matricula')+'\n'+alunoObject.get('Centro')
        homePage.text_msg = text_msg
        
        if (self.service_state == '0'):
            homePage.text_msg = homePage.text_msg + "\n[color=ff0000]Monitoramento automatico: [b]DESATIVADO[/b][/color]"
        else:
            homePage.text_msg = homePage.text_msg + "\nMonitoramento automatico: [color=00aa00][b]ATIVADO[/b][/color]"
        
        homePage.materias.height = 0 #Hack
        self.paginas.add_widget(homePage)
        
        for materia in alunoObject.get('Materias'):
            #Adiciona resultados parciais na Home
            homePageMateria = pageHomeMateria()
            homePageMateria.codigo = materia['Cod']
            homePageMateria.nota = (str("%.1f" % materia['MediaParcial']) if materia['MediaParcial']!=None else 'N.Pub') 
            homePage.materias.add_widget(homePageMateria)
            homePage.materias.height += homePageMateria.height #Hack
            
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