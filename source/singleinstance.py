import sys, threading, socket, SocketServer, datetime
from Queue import Queue
from select import select

class SingleInstance():
    _port = None
    _output = None
    _thread = None
    _server = None
    _serverup = None
    
    def __init__(self, port, output=True):
        self._port = port
        self._output = output
        
        try:
            #Connect and send message
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", self._port))
            sock.send(' '.join(sys.argv))
            
            #Wait for reply
            response = None
            timeout = 1
            sock.setblocking(0)
            ready = select([sock], [], [], timeout)
            if ready[0]:
                response = sock.recv(1024)
            
            #Check response
            if response == None: #No response (probably there's no server) 
                raise socket.error(111)
            elif response <> "ACK":
                self.out("Unknown response")
                raise SingleInstanceException("Server return an unknown response")
                
            #Close socket
            sock.close()
        except socket.error :
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            if exceptionValue[0] <> 111 :
                # don't actually know what happened ...
                raise SingleInstanceException("Socket returned an unknown error")
            else:
                try:                    
                    self._thread = threading.Thread(target=self.run)
                    self._thread.daemon = True
                    self._thread.name = "SingleInstance"
                    self._thread.start()
                except:
                    raise SingleInstanceException("Unable to create SingleInstance thread")
                
                timeout = datetime.datetime.now() + datetime.timedelta(seconds=5)
                while True:
                    if self._serverup == True:
                        print "break"
                        break
                    elif self._serverup == False:
                        raise SingleInstanceException("Unable to create server")
                    elif not self._thread.isAlive():
                        raise SingleInstanceException("Unable to create server")
                    elif datetime.datetime.now() > timeout:
                        self.kill()
                        print "aloow timeout"
                        raise SingleInstanceException("Unable to create server")
        else:
            self.out("Instance already exists. Exiting...")
            raise SingleInstanceException("Instance already exists")        
    
    def run(self):
        try:
            self._server = SingleInstanceServer(("127.0.0.1", self._port), SingleInstanceServerHandler)
        except:
            self._serverup = False
            raise SingleInstanceException("Unable to create SingleInstance server")
        self._serverup = True
        self._server.serve_forever()
    
    def kill(self):
        #try:
        self._server.kill()
        self._thread.join()
        self.out("Killed successfully")
        
        #except:
        #    raise SingleInstanceException("Unable to kill SingleInstance server")
    
    def out(self, message):
        if self._output:
            print "SingleInstance: "+message
                
    def newInstance(self):
        try:
            msg = self._server.messages.get(False)
            self._server.messages.task_done()
            return msg
        except:
            return None 

class SingleInstanceServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)

        if data[:3] <> "END":
            #Send callback
            self.server.messages.put(data)
            
            #Respond
            self.request.send("ACK")

class SingleInstanceServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    _exit = False
    messages = Queue()
    
    allow_reuse_address = True

    def serve_forever(self):
        #Serve until the exit flag is up
        while not self._exit:
            self.handle_request()
            
        #Close server
        self.server_close()
    
    def kill(self):
        #Set exit flag
        self._exit = True
        
        #Send a message to exit
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server_address[0], self.server_address[1]))
        sock.send("END")
        sock.close()

class SingleInstanceException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    import time
    try:
        instance = SingleInstance(10103)
    except SingleInstanceException as e:
        sys.exit(1)
    
    while True:
        try:
            msg = instance.newInstance()
            if msg <> None:
                print "NewInstance: "+msg
            time.sleep(.1)
        except KeyboardInterrupt:
            instance.kill()
            sys.exit(0)