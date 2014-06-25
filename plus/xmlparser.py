#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
    xmlObject.py
    
    XXX
    
    Metodos publicos
        XXX
        
    Dependencias (dentro do projeto)
        
'''

from lxml.etree import XML

class aluno:
    xmlData = None
    alunoData = None
    
    def get(self, key):
        try: return self.alunoData[key]
        except: return None
    
    def __init__(self, xmlData):
            self.xmlData = xmlData
            self.alunoData = {}
            xmlObject = XML(xmlData)
            
            #Verifica root tag
            if xmlObject.tag <> "SigmaWeb":
                raise AlunoException("Invalid root tag '"+xmlObject.tag+"'")
            
            for categoria in xmlObject:
                if categoria.tag == "Aluno":
                    for info in categoria: 
                        self.alunoData[info.tag] = info.text  
                
                elif categoria.tag == "Materias":
                    self.alunoData['Materias'] = []
                    for materia in categoria:
                        if materia.tag == "Materia":
                            dadosMateria = {
                                           'Nome'  : materia.get("Nome"), 
                                           'Cod'   : materia.get("COD"), 
                                           'Turma' : materia.get("Turma"), 
                                           'Centro': materia.get("Centro"),
                                           'Notas' : [],
                                           'MediaParcial': None,
                                           'Exame'       : None,
                                           'ExameReq'    : None,
                                           'MediaFinal'  : None
                                           }
                            
                            for nota in materia:
                                if nota.tag == "Nota":
                                    dadosMateria['Notas'].append({'Peso': nota.get("Peso").replace('%',''), 'Desc': nota.get("Desc"), 'Valor': self._float(nota.text, True)})
                                elif nota.tag == "Exame":
                                    dadosMateria['Exame'] = self._float(nota.text, True)
                                elif nota.tag == "MediaFinal":
                                    dadosMateria['MediaFinal'] = self._float(nota.text, True)
                            
                            mediaParcial, somaPesos, notasPublicadas = [0, 0, 0]
                            for nota in dadosMateria['Notas']:
                                if (nota['Valor'] != None): 
                                    notasPublicadas += 1
                                    mediaParcial += self._float(nota['Valor']) * self._float(nota['Peso'])
                                    somaPesos += self._float(nota['Peso'])
                            
                            if dadosMateria['MediaFinal'] <> None: dadosMateria['MediaParcial'] = dadosMateria['MediaFinal']
                            elif dadosMateria['Exame'] <> None: dadosMateria['MediaParcial'] = ((mediaParcial / somaPesos) * 0.6 + dadosMateria['Exame']*0.4) 
                            elif (notasPublicadas > 0): dadosMateria['MediaParcial'] = mediaParcial / somaPesos
                            else: dadosMateria['MediaParcial'] = None
                            
                            if (notasPublicadas == len(dadosMateria['Notas'])): dadosMateria['ExameReq'] = (5 - (mediaParcial*0.6))/0.4
                            else: dadosMateria['ExameReq'] = None
                            
                            self.alunoData['Materias'].append(dadosMateria)
    
    '''
    Funcao privada de float. Tenta dar um float, caso não consiga, o retorno depende da flag 'text' e do valor enviado
        num = None: Retorna None
        True: Retorna o proprio valor em str
        False: Retorna 0.0 
    '''
    def _float(self, num, text=False):
        if num == None: return None
        try: return float(num)
        except: return num if text else 0.0 
            
class AlunoException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)