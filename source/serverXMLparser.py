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
    
    materias = None
    
    def __init__(self, xml_data):
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
                        
                        notas_obj = []
                        exame = ""
                        for nota in materia:
                            if nota.tag == "Nota":
                                nota_obj = {'Peso': nota.get("Peso"), 'Desc': nota.get("Desc"), 'Valor': nota.text}
                                notas_obj.append(nota_obj)
                            elif nota.tag == "Exame":
                                exame = nota.text
                            else:
                                raise alunoXMLError("Expecting 'Nota' or 'Exame' tag: "+nota.tag)
                        
                        materia_obj = {'Nome': materia.get("Nome"), 'Cod': materia.get("COD"), 'Turma': materia.get("Turma"), 'Centro': materia.get("Centro"), 'Notas': notas_obj, 'Exame': exame}
                        
                        
                        #Coloca a materia na arrai materias
                        self.materias.append(materia_obj)
            
class alunoXMLError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)