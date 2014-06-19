#!/usr/bin/python
# -*- coding: UTF-8 -*-

import lxml.etree

class alunoXML:
    nome = None
    matricula = None
    tipoAluno = None
    status = None
    semestre = None
    centro = None
    
    time = None
    hash = None
    
    materias = None
    
    def __init__(self, time, hash, xml_data):
            self.time = time
            self.hash = hash
            self.materias = []
            
            XML = lxml.etree.XML(xml_data)
            
            #Verifica root tag
            if XML.tag <> "SigmaWeb":
                raise alunoXMLError("Invalid root tag: "+XML.tag)
            
            for dado in XML:
                if dado.tag == "Aluno":
                    for info in dado:
                        if info.tag == "Nome":
                            self.nome = info.text
                        elif info.tag == "Matricula":
                            self.matricula = info.text
                        elif info.tag == "TipoAluno":
                            self.tipoAluno = info.text
                        elif info.tag == "Status":
                            self.status = info.text
                        elif info.tag == "Semestre":
                            self.semestre = info.text
                        elif info.tag == "Centro":
                            self.centro = info.text   
                
                elif dado.tag == "Materias":
                    for materia in dado:
                        if materia.tag <> "Materia":
                            raise alunoXMLError("Expecting 'Materia' tag: "+materia.tag)
                        
                        conjuntoNotas = []
                        valorExame = None
                        valorMediaParcial = 0
                        valorExameReq = None
                        valorMediaFinal = None
                        totalNotasPublicadas = 0
                        totalNotas = 0
                        somaPesos = 0
                        for nota in materia:
                            if nota.tag == "Nota":
                                totalNotas = totalNotas + 1
                                if (nota.get("Peso")<>None):
                                    valorPeso = int(nota.get("Peso").replace("%",""))
                                else:
                                    valorPeso = None
                                
                                if (nota.text<>None):
                                    valorNota = float(nota.text)
                                else:
                                    valorNota = None
                                                                
                                if valorNota <> None:
                                    totalNotasPublicadas = totalNotasPublicadas + 1
                                    valorMediaParcial = valorMediaParcial + (valorNota * valorPeso)
                                    somaPesos = somaPesos + valorPeso
                                    
                                conjuntoNotas.append({'Peso': valorPeso, 'Desc': nota.get("Desc"), 'Valor': valorNota})
                            elif nota.tag == "Exame":
                                if (nota.text<>None):
                                    valorExame = float(nota.text)
                                else:
                                    valorExame = None
                            elif nota.tag == "MediaFinal":
                                if (nota.text<>None):
                                    valorMediaFinal = float(nota.text)
                                else:
                                    valorMediaFinal = None
                            else:
                                raise alunoXMLError("Expecting 'Nota' or 'Exame' tag: "+nota.tag)
                        
                        if totalNotasPublicadas > 0:
                            valorMediaParcial = valorMediaParcial / somaPesos
                        else:
                            valorMediaParcial = None
                        
                        if (totalNotasPublicadas == totalNotas) and (totalNotas > 0):
                            if valorMediaParcial >= 7:
                                valorExameReq = 0
                            else:
                                valorExameReq = (5 - (valorMediaParcial*0.6))/0.4
                                
                        
                        conjutoMateria = {
                                          'Nome': materia.get("Nome"), 
                                          'Cod': materia.get("COD"), 
                                          'Turma': materia.get("Turma"), 
                                          'Centro': materia.get("Centro"), 
                                          'Notas': conjuntoNotas, 
                                          'Exame': valorExame, 
                                          'MediaParcial': valorMediaParcial, 
                                          'ExameReq': valorExameReq, 
                                          'MediaFinal': valorMediaFinal
                                          }
                        
                        
                        #Coloca a materia na arrai materias
                        self.materias.append(conjutoMateria)
            
class alunoXMLError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)