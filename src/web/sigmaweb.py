#!/usr/bin/python
# -*- coding: UTF-8 -*-

import web.http
import lxml.etree

class SigmaWebPage:
    HTTP = None
    Cookies = None
    
    def __init__(self):
        self.HTTP = web.http.HTTP()
        self.Cookies = None
    
    def Login(self, username, password, verbose=False):
        Page = 'http://sigmaweb.cav.udesc.br/sw/sigmaweba.php'
        Post_Data = {'LSIST': 'SigmaWeb', 'LUNID': 'UDESC', 'lusid': username, 'luspa': password, 'opta': 'Login'}
        
        try:
            Response = self.HTTP.GetPageResponse(Page, Post_Data)
            if self.Erro(Response): 
                if verbose == False:
                    return False
                else:
                    return self.Erro(Response) 
        except:
            return False
        else:
            HTML = lxml.etree.HTML(Response.Data())
            if HTML[0][0].tag == "meta":
                #Login successful
                self.Cookies = Response.Cookies()                
                return True
            else:
                #Login failed
                return False
    
    def Home(self):
        Page = 'http://sigmaweb.cav.udesc.br/sw/sigmaweb0.php'
        
        try:
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        else:
            return Response
        
    def ResultadosSemestraisAcademico(self, Ano=None):
        if self.Home() == None:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb1.php?var=R6645"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb4.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb6.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        if Ano == None:
            return Response
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb7.php"
            Post_Data = {'nseme': Ano, 'opta': 'Avancar'}
            Response = self.HTTP.GetPageResponse(Page, Post_Data, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb7.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        return Response
    
    def ResultadosParciaisDiario(self, Diario=None):
        if self.Home() == None:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb1.php?var=R6655"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb4.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb5.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        if Diario==None:
            return Response
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb7.php"
            Post_Data = {'nagru': Diario, 'opta': 'Enter'}
            Response = self.HTTP.GetPageResponse(Page, Post_Data, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb7.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response)=="Não há registro de notas parciais": 
                return []
            elif self.Erro(Response) <> False:
                return None
        except:
            return None
        
        return Response
    
    def ResultadosSemestraisDiario(self, Ano=None, Diario=None):
        if self.Home() == None:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb1.php?var=R6650"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb4.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        if Ano == None:
            return Response
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb5.php"
            Post_Data = {'nseme': Ano, 'opta': 'Avancar'}
            Response = self.HTTP.GetPageResponse(Page, Post_Data, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb6.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        if Diario==None:
            return Response
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb7.php"
            Post_Data = {'nagru': Diario, 'opta': 'Enter'}
            Response = self.HTTP.GetPageResponse(Page, Post_Data, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb7.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        return Response
    
    def ConsultaDiario(self, Ano, Diario):
        if self.Home() == None:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb1.php?var=R6605"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb4.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        if Ano == None:
            return Response
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb5.php"
            Post_Data = {'nseme': Ano, 'opta': 'Avancar'}
            Response = self.HTTP.GetPageResponse(Page, Post_Data, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb6.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        if Diario==None:
            return Response
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb7.php"
            Post_Data = {'nagru': Diario, 'opta': 'Enter', 'nmail': '1'}
            Response = self.HTTP.GetPageResponse(Page, Post_Data, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb7.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        return Response
    
    def HistoricoEscolar(self):
        pass
    
    def BoletimGradeAptidao(self):
        if self.Home() == None:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb1.php?var=R6140"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb4.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb5.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb6.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        return Response
    
    def Foto(self):
        Home = self.Home()
        if Home == None:
            return None
        
        Response_Data = Home.Data()
        
        HTML = lxml.etree.HTML(Response_Data)
        
        try:
            FotoURL = HTML[1][2][0][2][0][0][0][0].get("src")
        except:
            return False
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/" + FotoURL
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        return Response
        
    
    def Curriculo(self):
        pass
    
    def AtualizaEndereco(self):
        pass
    
    def ConsultaMatriculaAcademico(self):
        pass
    
    def ConsultaOferecimentoDisciplina(self):
        pass
    
    def ListaTurmasOferecidas(self):
        if self.Home() == None:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb1.php?var=R6113"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb4.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb5.php"
            Post_Data = {'ncrid': 'T', 'ndpco': 'all', 'opta': 'Avancar'}
            Response = self.HTTP.GetPageResponse(Page, Post_Data, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        try:
            Page = "http://sigmaweb.cav.udesc.br/sw/sigmaweb5.php"
            Response = self.HTTP.GetPageResponse(Page, { }, {'Cookie' : self.Cookies})
            if self.Erro(Response): return None
        except:
            return None
        
        return Response
    
    def ConsultaCoeficienteRanking(self):
        pass
    
    def SaldoVagas(self):
        pass
    
    def Erro(self, Response):
        Response_Data = Response.Data()
        
        if Response_Data.count("</html>") > 1:
            Response_Data = Response_Data.split("</html>")
            Response_Data = Response_Data[1]
        
        HTML = lxml.etree.HTML(Response_Data)
        
        try:
            Error = HTML[1][1][0][0].text
        except:
            return False
        else:
            if Error == "ERRO:":
                return str(HTML[1][1][1][0].text)
            else:
                return False
        