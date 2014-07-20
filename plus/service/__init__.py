#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
    service.__init.py__
    
    O objetivo deste arquivo é descrever a classe Service(). Esta classe tem como funcao
    inicializar/finalizar o service e manter (com o service) uma lista sincronizadas de 
    variaveis
    
    Metodos publicos
        void  start   (dict data)
        void  stop    (void)
        bool  isAlive (void)
        int   getState(void)
        str   getKey  (str key)
        void  setKey  (str key, str value)
        list  getKeys (void)
        
    Dependencias (dentro do projeto)
        threadcomm.py
'''

#Import LIBs
from threading import Thread, currentThread
from kivy.utils import platform
from debug import Debug
from notification.notification import Notification
from time import sleep, time

#Import project files
from threadcomm import ThreadComm, ThreadCommException, ThreadCommClient

STATE_NOTSTARTED       = 1
STATE_CONNECTING       = 2
STATE_CONNECTEDTHREAD  = 3
STATE_CONNECTEDANDROID = 4
STATE_CONNECTEDREMOTE  = 5
STATE_DISCONNECTING    = 6

class Service():
    #Configuracoes do ThreadComm
    CONFIG_THREADCOMMPORT = 51352
    CONFIG_THREADCOMMID = "sigmawebplus"
    
    #Variaveis
    _state = STATE_NOTSTARTED
    _formerState = STATE_NOTSTARTED
    _forceThread = None
    _androidTrigger = False #Hack: O service do Android soh pode ser aberto pelo main thread. Uso essa flag para avisar o main thread a hora de abrir
    _androidTriggerEnd = False
    _androidService = None #Guarda do ponteiro do Android Service, para poder fechar depois
    _lastDisconnection = 0 #Essa variavel serve para ter um timeout de 5 segundos entre cada reconexao
    
    #Objetos
    _threadComm = None #Ponteiro para o objeto do ThreadComm (utilizado para se comunicar com o service)
    _data = None       #Objeto 'Dict' utilizado para armazenar todos as propriedade que estão sinronizadas com o service
    
    '''
    Salva os dados recebido como parametro e inicializa o servico de forma assincrona
    Nota: Se o service já existir, os dados serão sobreescritos em favor dos dados do service
    '''
    def start(self, data, forceThread=False):
        if (self.getState() == STATE_NOTSTARTED):
            Debug().note('service.start(): Iniciando server')
            self._setState(STATE_CONNECTING)
            self._data = data #Salva dados no objeto
            self._forceThread = forceThread
            thread = Thread(target=self._start, name='service._start()') #Faz a inicializacao do Service em outro thread
            thread.daemon = False
            thread.start()
        else:
            Debug().note('service.start(): Reiniciando server')
            thread = Thread(target=self._restart, name='service._restart()', args=(data, forceThread))
            thread.daemon = False
            thread.start()
    
    '''
    Manda um aviso para o service se finalizar e espera a resposta do service!
    ATENCAO: Essa funcao eh bloqueante. Ela trava o andamento do programa ateh receber o sinal do service!
    '''
    def stop(self, killService=True):
        while (self.getState() == STATE_CONNECTING): sleep(0.1) #Espera o ThreadComm conectar, caso ele esteja no modo 'Conectando'
        if self.isAlive():
            self._setState(STATE_DISCONNECTING)
            self._stop(killService)
        else:
            Debug().warn('service.stop(): Service nao esta rodando. Nada para parar! CurrentState: '+str(self.getState()))
            
    
    '''
    Retorna True se o service esta conectado e pronto para funcionar
    '''
    def isAlive(self):
        if (self.getState() == STATE_CONNECTEDTHREAD) or (self.getState() == STATE_CONNECTEDANDROID) or (self.getState() == STATE_CONNECTEDREMOTE):
            return True
        else: return False
    
    '''
    Retorna o estado que o objeto se encontra. Uma lista de estados pode ser vista no inicio desse arquivo
    '''
    def getState(self):
        return self._state
    
    def getFormerState(self):
        return self._formerState
    
    '''
    Retorna o valor da chave solicitada
    '''
    def getKey(self, key):
        try: return str(self._data[key])
        except: return ''
    
    '''
    Seta o valor da chave e avisa o service desta mudanca
    '''
    def setKey(self, key, value):
        self._data[key] = str(value)
        if self.isAlive(): self._sendKey(key)
    
    '''
    Este metodo faz o objeto buscar se há novas mensagens no ThreadComm
    Retorna uma lista com as keys e valores de todas os dados modificados [[key1, value1], [key2, value2], ...]
    Nota: Ele não vai retornar a key se o valor recebido for igual o valor já presente!
    Nota2: Ele tambem é responsavel pelo main loop do service (ele responde outros tipos de mensagens)
    Nota3: A logica do loop foi movida para a funcao _parseMessage() para melhorar a leitura
    '''
    def getKeys(self):
        self._startAndroid() #Hack: O service do Android soh pode ser aberto pelo main thread. Uso essa funcao para o main thread verificar se deve abrir ou nao
        if not self.isAlive(): return None #Verifica se o servidor esta conctado
        
        returnData = []
        while True:
            #Busca novas mensagens no ThreadCom
            try: message = self._threadComm.recvMsg()
            except: break
            
            #Faz o parse da mensagem recebida e, se o valor retornado não for nulo, adiciona na returnData
            data = self._parseMessage(message)
            if data is not None: returnData.append(data)
        
        return returnData
    
    '''
    ''   PRIVATE METHODS
    '''
    
    def __init__(self):
        self._data = {}
    
    def _setState(self, value):
        self._formerState = self._state
        self._state = value
    
    def _restart(self, data, forceThread=False):
        Debug().note('service._restart()')
        self.stop()
        self.start(data, forceThread)
    
    '''
    Metodo interno para iniciar o service. Ele primeiro vai verificar se o service já não está rodando
    Se o service já estiver rodando, ele salva o ponteiro do ThreadComm e solicita ao service todas os seus dados
    Se o service não estiver rodando, ele chama o metodo _startService() para inicializar o service 
    '''
    def _start(self):
        Debug().note('service._start()')
        
        while not (self._lastDisconnection+1 < time()):
            sleep(0.1)
        
        self._threadComm = ThreadComm(self.CONFIG_THREADCOMMPORT, self.CONFIG_THREADCOMMID, ThreadCommClient)
        try: self._threadComm.start()
        except ThreadCommException as e: #Servico nao esta rodando
            Debug().note('service._start(): Service nao esta aberto')
            self._startService()
        else: #Servico já esta rodando
            Debug().note('service._start(): Service ja esta aberto')
            self._threadComm.sendMsg("AKEY") #Solicita todas as keys que o server tem disponivel!
            if (self._forceThread == False) or (platform != 'android'): self._setState(STATE_CONNECTEDREMOTE)
            else:
                Debug().warn('service._start(): Finalizando service e abrindo denovo para atender a forceThread')
                currentData = self._data
                self._stop()
                self.start(currentData, True)
    
    '''
    Metodo que inicializa o service de acordo com a plataforma
    Ele inicializa o service e depois conecta o ThreadComm com o service
    '''
    def _startService(self):
        if (platform == 'android') and (not self._forceThread): connectThread = False
        else: connectThread = True
        
        if not connectThread:
            Debug().note('service._startService(): Esperando o _androidTrigger')
            self._androidTrigger = True #Hack: Ativa a flag para abrir o service do android. O android soh deixa o service ser aberto pelo main thread
            while (self._androidTrigger == True): pass #Espera o service abrir
        else:
            from main import MainService
            mainService = MainService()
            thread = Thread(target=mainService.run)
            thread.daemon = False
            thread.name = "MainService"
            thread.start()
            
        Debug().note('service._startService(): Esperando o ThreadComm conectar')
        while True: #Todo: Colocar um timeout
            try: self._threadComm.start()
            except ThreadCommException: pass
            else: break
        
        Debug().note('service._startService(): Enviando todos os dados')
        for key in self._data:
            self._sendKey(key)
        self._threadComm.sendMsg("STRT") #Sinal para o Service iniciar
        
        #Aguarda a resposta do service
        Debug().note('service._startService(): Aguardando o service ser iniciado')
        message = None
        while message != 'STRT':
            try: message = self._threadComm.recvMsg()
            except: pass
        
        if connectThread: self._setState(STATE_CONNECTEDTHREAD)
        else: self._setState(STATE_CONNECTEDANDROID)
    
    '''
    Metodo utilizado para fazer um parse da mensagem recebida e reagir conforme
    Retorna: Uma lista [key, value] se a mensagem for do tipo "SKEY" e o valor recebido for diferente do que já está na self._data
    '''
    def _parseMessage(self, message):
        if message[:4] == "SKEY": #Set key
            #Extrai dados da mensagem
            length = int(message[4:6]) 
            key, value = [message[6:6+length], message[6+length:]]
            
            '''
            Se o valor for diferente do que está salvo:
                * Salva o novo valor
                * Retorna o nome da chave e seu respectivo valor
            '''
            if value <> self.getKey(key):
                self._data[key] = value
                return key, value
        elif message[:4] == "GKEY": #Get key
            key = message[4:]  #Extrai o nome da key na mensagem
            self._sendKey(key) #Manda o valor da key de volta para o service
        elif message[:4] == "AKEY": #Get all keys
            for key in self.data:
                self._sendKey(key)
        elif message[:4] == "NOTI": #Send a notification
            notificationMsg = message[4:].split("|")
            notificationObject = Notification(*notificationMsg)
            notificationObject.enableActivity = True #O notification normalmente funciona no Service, isso serve para mudar o modo para Activity
            notificationObject.notify()
        elif message[:4] == "STOP": #O Service foi finalizado de forma inesperada
            self._stop(False, True)
            Debug().error('Service finalizado de forma inesperada. O applicativo esta sendo fechado de forma forcada')
            return ['app_delete', '1']
    
    '''
    Metodo privado que envia para o service a KEY especificada, no formato especificado
    Voce nao precisa informar o valor, ele pega direto do self._data
    '''
    def _sendKey(self, key):
        length = str(len(key)).zfill(2)
        self._threadComm.sendMsg("SKEY"+length+key+self.getKey(key))
    
    '''
    O service do Android soh pode ser aberto pelo main thread. 
    Essa funcao verifica uma flag de aberura. Caso ela esteja ligada, ele abre o Service e desliga a flag
    '''
    def _startAndroid(self):
        if self._androidTrigger:
            Debug().note('service._startAndroid(): Iniciando o service no Android')
            from android import AndroidService
            print "antes3"
            self._androidService = AndroidService('SigmaWeb+', 'Monitorando')
            print "durante3" 
            self._androidService.start()
            print "depois 3"
            self._androidTrigger = False
        
        if self._androidTriggerEnd:
            Debug().note('service._startAndroid(): Finalizando o service no Android')
            print "antes 2"
            if self._androidService is not None:
                self._androidService.stop()
            else:
                Debug().warn('service._startAndroid(): Service nao pode ser finalizado. Nao esta aberto')
            print "depois 2"
            self._androidService = None
            self._androidTriggerEnd = False
    
    '''
    Para o service do android caso ele esteja iniciado
    '''
    def _stopAndroid(self):
        Debug().note('service._stopAndroid()')
        if (platform == 'android') and (self.getFormerState() == STATE_CONNECTEDREMOTE):
            from android import AndroidService
            print "antes1"
            self._androidService = AndroidService('SigmaWeb+', 'Monitorando')
            print "depois 1"
        
        if (self._androidService != None):
            Debug().note('service._stopAndroid(): Esperando o _androidTriggerEnd') 
            self._androidTriggerEnd = True
            if currentThread().name == 'service._restart()':
                while self._androidTriggerEnd: sleep(0.1)
            else:
                self._startAndroid()
    
    '''
    Funcao privada para parar o service (ela nao faz checks se o service foi iniciado. Isso eh trabalho da funcao publica)
    '''
    def _stop(self, killService=True, forceKillAndroid=False):
        if killService: 
            self._threadComm.sendMsg("KILL") #Manda o sinal para o service terminar
            
            '''
            A maneira que esta funcao verifica se o service foi desconectado eh a seguinte:
                1) Espera o service mandar uma mensagem STOP (avisando que está quase sendo desligado)
                2) Flooda o service com mensagens NULL, ateh que elas comecem a retornar erro
            '''
            Debug().note('service.stop(): Aguardando o service ser desligado')
            message = None
            while message != 'STOP':
                try: message = self._threadComm.recvMsg()
                except: pass
            while True:
                try: self._threadComm.sendMsg("NULL")
                except: break
                sleep(0.1)
                
        Debug().note('service.stop(): Limpando a memoria')
        #Limpa a memoria e limpa o estado do objeto
        self._threadComm.stop()
        if killService or forceKillAndroid: self._stopAndroid()
        self._data = None
        self._threadComm = None
        self._setState(STATE_NOTSTARTED)
        self._lastDisconnection = time()
        