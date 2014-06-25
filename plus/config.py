#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
    config.py
    
    Este arquivo descreve a classe UserConfig que é um wrapper para as funcoes de config do kivy. Para este objeto 
    funcionar, voce deve fornecer na sua inicializacao um pointeiro para o objeto de configuracao do kivy.
    
    Metodos publicos
        str   getConfig    (str key)
        void  setConfig    (str key, str value[, bool write])
        list  getConfigs   (list configs)
        void  setConfigs   (list configs[, bool write])
        void  clearConfig  (void)
        list  exportConfig (void)
        void  write        (void)
        
        
    Dependencias (dentro do projeto)
        
'''

class UserConfig:
    defaultSection = None
    defaultConfig = None
    kivyConfig = None
    
    '''
    Retorna o valor de uma chave especifica
    '''
    def getConfig(self, key):
        return self.kivyConfig.get(self.defaultSection, key)
    
    '''
    Seta o valor de uma chave especifica. Pode-se utilizar o parametro 'write' para atrasar o salvamento no disco
    '''
    def setConfig(self, key, value, write=False):
        self.kivyConfig.set(self.defaultSection, key, value)
        if write: self.write()
    
    '''
    Retorna uma lista com key e valor de varias chaves especificadas
    '''
    def getConfigs(self, configs):
        for key in configs:
            configs[key] = self.getConfig(key)
        return configs
    
    '''
    Seta o valor de varias chaves. Pode-se utilizar o parametro 'write' para atrasar o salvamento no disco
    '''
    def setConfigs(self, configs, write=False):
        for key in configs:
            self.setConfig(key, configs[key])
        if write: self.write()
    
    '''
    Restaura todas as configuracoes para o valor inicial
    '''
    def clearConfig(self):
        self.setConfigs(self.defaultConfig)
    
    '''
    Retorna uma lista contendo a key e valor de todas as chaves default
    '''
    def exportConfig(self):
        return self.getConfigs(self.defaultConfig)
    
    '''
    Salva os dados no disco
    '''
    def write(self):
        self.kivyConfig.write()
    
    '''
    ''   PRIVATE METHODS
    '''
    
    def __init__(self, kivyConfig, defaultSection, defaultConfig):
        self.kivyConfig = kivyConfig
        self.defaultSection = defaultSection
        self.defaultConfig = defaultConfig
        self.kivyConfig.setdefaults(self.defaultSection, self.defaultConfig)