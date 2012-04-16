import socket
import select
import time

from Signals import SignalObject, Signal

class MasterClient(object):
    def __init__(self, socket_manager, sock, address):
        self.socket_manager = socket_manager
        self.address = address
        self.socket = sock
        
        #limit the buffer to 128 characters until they have been authenticated
        self.buffer_limit = 128
        
        self.buffer = ""
        
    def unlimit(self):
        self.buffer_limit = -1
        
    def send(self, datum):
        self.socket.send(datum)
        
    def disconnect(self):
        self.socket_manager.handle_disconnect(self.socket)
        self.socket_manager.disconnect.emit(self)
        self.socket.close()
        
    def handle(self):
        data = self.socket.recv(1024)
        if len(data) <= 0:
            self.disconnect()
            return
        self.buffer += data
        
        if self.buffer_limit != -1 and len(self.buffer) > self.buffer_limit:
            self.disconnect()
            return
        
        next_nl_pos = self.buffer.find("\n")
        while next_nl_pos != -1:
            datum, self.buffer = self.buffer.split('\n', 1)
            self.handle_datum(datum)
            next_nl_pos = self.buffer.find("\n")
        
    def handle_datum(self, datum):
        datum = datum.split()
        self.socket_manager.request.emit(self, datum)

class SocketManager(SignalObject):
    
    started = Signal
    stopped = Signal
    update = Signal
    connect = Signal
    request = Signal
    disconnect = Signal

    def __init__(self, master_ip, master_port, max_clients):
        SignalObject.__init__(self)
    
        self.master_clients = {}
    
        self.master_ip = master_ip
        self.master_port = master_port
    
        self.running = True
        self.interval = 3800
        self.next_update = time.time() + self.interval
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((master_ip, master_port))
        self.socket.listen(max_clients)
        
    def run(self):
        self.started.emit(self.master_ip, self.master_port)
        try:
            while self.running:
                if time.time() >= self.next_update:
                    self.update.emit()
                    self.next_update = time.time() + self.interval
                
                wait_time = self.next_update - time.time()
                
                wait_devs = [self.socket] + self.master_clients.keys()
                
                try:
                    rfds, wfds, efds = select.select(wait_devs, [], [], wait_time)
                
                    for rfd in rfds:
                        if rfd == self.socket:
                            self.handle_connect()
                        else:
                            self.master_clients[rfd].handle()
                            
                except select.error:
                    pass
        except KeyboardInterrupt:
            self.stopped.emit()
                
    def handle_connect(self):
        sock, address = self.socket.accept()
        self.master_clients[sock] = MasterClient(self, sock, address)
        self.connect.emit(self.master_clients[sock])

    def handle_disconnect(self, sock):
        del self.master_clients[sock]