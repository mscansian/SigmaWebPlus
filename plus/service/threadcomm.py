import sys, threading, socket, time
from Queue import Queue
from select import select

class ThreadComm():
    #Objects
    netObject = None
    
    #Configuration
    _port = None
    _connID = None
    _role = None
    
    def __init__(self, port, connID, role=None):
        self._port = port
        self._connID = connID
        self._role = role
    
    def start(self):
        try:
            client = ThreadCommClient(self._port, self._connID)
            response = client.start()
        except ThreadCommException:
            response = False
        
        if (response == False): #No server available
            if (self._role==None) or (self._role==ThreadCommServer): 
                #Close client and start a new server
                client.stop()
                
                server = ThreadCommServer(self._port, self._connID)
                server.start()
                server.waitReady()
                self.netObject = server
                return True
            elif (self._role==ThreadCommClient): #Raise no server available error
                raise ThreadCommException("Server not available in ThreadComm.start()")
            else: #Raise unknown role error
                raise ThreadCommException("Unknown role in ThreadComm.start()")
        else: #Server is available
            if (self._role==None) or (self._role==ThreadCommClient): #Keep client connection
                self.netObject = client
                return True
            elif (self._role==ThreadCommServer): #Raise server already up error
                raise ThreadCommException("Server already up in ThreadComm.start()")
            else: #Raise unknown role error
                raise ThreadCommException("Unknown role in ThreadComm.start()")
                    
    def stop(self):
        return self.netObject.stop()
    
    def recvMsg(self):
        return self.netObject.recvMsg()
    
    def sendMsg(self, message):      
        return self.netObject.sendMsg(message)

    def isReconnect(self):
        return self.netObject.isReconnect()

class ThreadCommClient():
    #Objects
    socket = None
    
    #Configurations
    _port = None
    _connID = None
    _messages = None
    _reconnect = None
    
    #Signals
    _READY = False
    
    def __init__(self, port, connID):
        self._port = port
        self._connID = connID
    
    def start(self):
        try:
            response = None
            
            #Create socket and try a connection
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(("127.0.0.1", self._port))
            self.socket.sendall('SIN '+self._connID)
                
            #Wait for a reply and handle it acordingly
            self.socket.setblocking(0)
            ready = select([self.socket], [], [], 1)
            if ready[0]:
                response = self.socket.recv(1024)
        except socket.error:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            if (exceptionValue[0] == 111) or (exceptionValue[0] == 104):
                raise ThreadCommException("Server did not respond on ThreadCommClient.start()")
            else:
                raise
        
        if  not (response == "ACK "+self._connID):
            raise ThreadCommException("Server returned an unknown response on ThreadCommClient.start()")
        
        self._READY = True
        return True
    
    def stop(self):
        self.socket.close()
    
    def waitReady(self, timeout=0):
        while not self._READY:
            time.sleep(0.1)
    
    def recvMsg(self):
        self._listen()
        return self._getMessage()
    
    def sendMsg(self, message):
        if self.socket == None:
            raise ThreadCommException("Socket not connected to the server in ThreadCommClient.sendMsg()")
        self.socket.sendall(message.replace("\n","\\n")+"\r\n")
    
    def _listen(self):
        data = ""
        while True:
            ready = select([self.socket], [], [], 0.01)
            if ready[0]:
                data = data + self.socket.recv(1024)
                if data == "":
                    break
            else:
                break
            
        data = data.splitlines()
        for line in data:
            if line <> "":                 
                self._addMessage(line)
                    
    def _addMessage(self, message):
        if self._messages == None:
            self._messages = Queue()
        self._messages.put(message.replace("\\n","\n"))

    def _getMessage(self):
        try:
            message = self._messages.get(False)
            self._messages.task_done()
            return message
        except:
            raise ThreadCommException("No new messages in ThreadComm._getMessage()")

class ThreadCommServer(): 
    #Objects
    server = None
    client = None
    
    #Configurations
    _port = None
    _connID = None
    _messages = None
    
    #Signals
    _SIGTERM = False
    _READY = False
    
    def __init__(self, port, connID):
        self._port = int(port)
        self._connID = str(connID)
    
    def start(self):
        try:                    
            self.thread = threading.Thread(target=self._serve)
            self.thread.daemon = False
            self.thread.name = "ThreadComm Server"
            self.thread.start()
        except:
            raise ThreadCommException("Unable to create ThreadComm thread in ThreadCommServer.start()")
    
    def stop(self):
        self._SIGTERM = True
    
    def waitReady(self):
        while not self._READY:
            time.sleep(0.1)
    
    def recvMsg(self):
        return self._getMessage()
    
    def sendMsg(self, message):
        if self.client == None:
            raise ThreadCommException("Client not connected to the server in ThreadCommServer.sendMsg()")
        self.client.sendall(message.replace("\n","\\n")+"\r\n")

    def _serve(self):       
        #Create a new server
        self.server = self._createServer(self._port)
        self._READY = True
        while not self._SIGTERM:
            client = None
            while client == None: #If there is not client, we should wait for a new one
                client = self._waitConnection(self.server, self._connID)
                if client <> None:
                    self.client = client
                else:
                    client = self.client
            
            #Get new client messages
            try:
                data = self._listen(self.client)
            except ThreadCommException:
                pass
            time.sleep(0.1)
        self._close(self.server, self.client)
        
    def _addMessage(self, message):
        if self._messages == None:
            self._messages = Queue()
        self._messages.put(message.replace("\\n","\n"))

    def _getMessage(self):
        try:
            message = self._messages.get(False)
            self._messages.task_done()
            return message
        except:
            raise ThreadCommException("No new messages in ThreadComm._getMessage()")

    #Start server socket at a given port and return its object
    def _createServer(self, port, timeout=0.0):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("127.0.0.1", port))
            server.settimeout(timeout)
        except:
            raise ThreadCommException("Unable to start server socket at ThreadCommServer._createServer()")
        
        return server
        
    #Wait for a client connection and return its object
    def _waitConnection(self, server, connID):
        server.listen(1)
        ready = select([server], [], [], 0.01)
        if ready[0]:
            client, addr = server.accept()
            data = client.recv(1024)
            if data == "SIN "+connID: #Valid connection
                client.sendall("ACK "+connID)
                return client
            else: #Invalid connection
                client.close()
        return None
    
    def _listen(self, client):
        data = ""
        while True:
            ready = select([client], [], [], 0.01)
            if not ready[0]:
                break
            
            try:
                line = client.recv(1024)
            except: pass
            else:
                if not line: break
                data = data + line
        
        if not (data == ""):
            data = data.splitlines()
            for msg in data:
                if msg <> "":                 
                    self._addMessage(msg)
        else:
            raise ThreadCommException("No available data in ThreadCommServer._listen()")
    
    def _close(self, server, client):
        client.close()
        server.shutdown(socket.SHUT_RDWR)
        server.close()

class ThreadCommException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)