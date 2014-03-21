#!/usr/bin/python
# -*- coding: UTF-8 -*-

import http, lxml.etree

class Aluno:    
    #Login info
    _Matricula = None
    _Senha = None
    
    #Basic Info
    _BasicInfoUpdate = False
    _Nome = None
    _SemestreCorrente = None
    _StatusSistema = None
    _Centro = None
    
    _SemestreMatricula = None
    _Coeficiente = None
    _Situacao = None
    
    #Foto
    _Foto = None
    
    #Materias
    _Materias = None
    
    def __init__(self, Matricula, Senha):
        self._Matricula = Matricula
        self._Senha = Senha

    def _UpdateBasicInfo(self):
        myPage = http.Page("http://sigmaweb.cav.udesc.br/sw/sigmaweba.php")
        myPage.set_RequestData(http.Data("LSIST", "SigmaWeb"), http.Data("LUNID", "UDESC"), http.Data("lusid", self._Matricula), http.Data("luspa", self._Senha), http.Data("opta", "Login"))
        try:
            myPage.Refresh()
        except http.HTTPError as e:
            raise SigmaWebError(e)
        
        try:
            HTML = lxml.etree.HTML(myPage.get_ResponseData())
            CheckString = HTML[0][0].tag
        except:
            raise SigmaWebError("Unable to parse HTML at "+myPage.get_URL())
        
        if CheckString <> "meta": #Login failed
            return False
        
        myCookies = myPage.get_ResponseCookies()
        myPage = http.Page("http://sigmaweb.cav.udesc.br/sw/sigmaweb0.php")
        myPage.set_RequestCookies(*myCookies)
        try:
            myPage.Refresh()
        except http.HTTPError as e:
            raise SigmaWebError(e)
        
        try:
            HTML = lxml.etree.HTML(myPage.get_ResponseData())
            self._SemestreCorrente = HTML[1][2][0][2][0][4][0].text.replace("Semestre: ", "")
            self._StatusSistema = HTML[1][2][0][2][0][5][0].text.replace("Status: ","").split(" - ")
            self._Centro = HTML[1][0][0][1].text
            self._Nome = HTML[1][0][0][2].text
        except:
            raise SigmaWebError("Unable to parse HTML at "+myPage.get_URL())
        
        self._BasicInfoUpdate = True

    def get_Nome(self, ForceUpdate=False):
        if (not self._BasicInfoUpdate) or ForceUpdate: self._UpdateBasicInfo()
        return self._Nome
    
    def get_Materias(self, ForceUpdate=False):
        pass

class Materia:
    _Nome = None
    _Codigo = None
    _Turma = None
    _Fase = None
    _CH = None
    _Creditos = None
    _DEP = None
    _Professor = None
    _NotasParciais = None #Salvar em uma array 1==> nota1, 2=> nota 2
    _NotaFinal = None
    _NotaExame = None
    _Creditos = None
    _Professor = None
    
    def get_Notas(self, ForceUpdate=False):
        pass
    
class Nota:
    _Nome = None
    _Valor = None
    _Peso = None
    
    def __init__(self, Nome, Valor, Peso):
        self._Nome = Nome
        self._Valor = Valor
        self._Peso = Peso
    
    def get_Nome(self):
        return self._Nome
    
    def get_Valor(self):
        return self._Valor
    
    def get_Peso(self):
        return self._Peso
    
class SigmaWebError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)