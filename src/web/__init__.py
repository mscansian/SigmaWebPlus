import sigmaweb, threading
import lxml.etree

class SigmaWeb:
    username = None
    password = None
    SigmaWeb = None
    Lock = None
    
    def __init__(self):
        self.SigmaWeb = sigmaweb.SigmaWebPage()
        self.Lock = threading.Lock()
        
    def ModificarDadosAcesso(self, username, password):
        self.Lock.acquire()
        self.username = username
        self.password = password
        self.Lock.release()
    
    def VerificarLogin(self):
        self.Lock.acquire()
        Login = self.SigmaWeb.Login(self.username, self.password, True)
        self.Lock.release()
        return Login
    
    def MeuNome(self):
        self.Lock.acquire()
        if self.SigmaWeb.Login(self.username, self.password) == False: 
            self.Lock.release()
            return None
        
        Response = self.SigmaWeb.Home()
        if Response == None: 
            self.Lock.release()
            return None
        
        HTML = lxml.etree.HTML(Response.Data())
        try:
            Nome = HTML[1][0][0][2].text
        except:
            self.Lock.release()
            return None
        
        self.Lock.release()
        return Nome

    def MinhasMaterias(self):
        self.Lock.acquire()
        if self.SigmaWeb.Login(self.username, self.password) == False: 
            self.Lock.release()
            return None
        
        Response = self.SigmaWeb.ResultadosParciaisDiario()
        if Response == None: 
            self.Lock.release()
            return None
        
        Materias = []
        
        HTML = lxml.etree.HTML(Response.Data())
        try:
            for option in HTML[1][4][0][2][0][0]:
                Materias.append([option.get("value"), str(option.text).replace(str(option.get("value")).split("/")[0]+" - ", "").replace(" - Turma: "+str(option.get("value")).split("/")[1],"")])
        except:
            self.Lock.release()
            return None
        
        self.Lock.release()
        return Materias
    
    def TodasMaterias(self):
        self.Lock.acquire()
        if self.SigmaWeb.Login(self.username, self.password) == False: 
            self.Lock.release()
            return None
        
        Response = self.SigmaWeb.ListaTurmasOferecidas()
        if Response == None: 
            self.Lock.release()
            return None
        
        Materias = []
        
        HTML = lxml.etree.HTML(Response.Data())
        
        try:
            for Row in HTML[1][1]:
                try:
                    Codigo = str(Row[3].text).replace(u"\xa0", "")
                    Materia = str(Row[4].text).replace(u"\xa0", "")
                    if Codigo <> "":
                        Materias.append([Codigo, Materia])
                except:
                    pass
        except:
            self.Lock.release()
            return None
        
        Materias.pop(0)
        
        self.Lock.release()
        return Materias
    
    def NotasParciais(self, Diario):
        self.Lock.acquire()
        if self.SigmaWeb.Login(self.username, self.password) == False: 
            self.Lock.release()
            return None
        
        Response = self.SigmaWeb.ResultadosParciaisDiario(Diario)
        if Response == None: 
            self.Lock.release()
            return None
        
        if Response == []: 
            self.Lock.release()
            return []
    
        HTML = lxml.etree.HTML(Response.Data())
        
        #Results
        Result = []
        
        try:
            Rowspan = int(HTML[1][1][0][0].get("rowspan"))
        except:
            Rowspan = 1
        
        Row = 0
        LineData = []
        for tr in HTML[1][1]:
            for td in tr:
                try:
                    LineData.append(str(td.text).replace(u"\xa0", ""))
                except:
                    self.Lock.release()
                    return None
            
            Row = Row + 1
            if Row == Rowspan:
                Row = 0
                Result.append(LineData)
                LineData = []
        
        self.Lock.release()
        return Result        