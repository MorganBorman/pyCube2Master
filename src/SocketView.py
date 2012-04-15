import socket
import select
import time

from Signals import SignalObject, Signal

class MasterClient(object):
    def __init__(self, socket_view, sock, address):
        self.socket_view = socket_view
        self.address = address
        self.socket = socket
        
        self.buffer = ""
        
    def handle(self):
        data = self.socket.recv(1024)
        if len(data) <= 0:
            self.socket_view.handle_disconnect(self.socket)
            self.socket.close()
            return
        self.buffer += data
        
	    next_nl_pos = self.remote_data_stream.find("\n")
	    while next_nl_pos != -1:
		    datum, self.remote_data_stream = self.remote_data_stream.split('\n', 1)
		    self.handle_datum(datum)
		    next_nl_pos = self.remote_data_stream.find("\n")
        
    def handle_datum(self, datum):
        pass

class SocketView(SignalObject):

    update = Signal

    def __init__(self, master_ip, master_port, max_clients):
        SignalObject.__init__(self)
    
        self.master_clients = {}
    
        self.running = True
        self.interval = 3800
        self.next_update = time.time() + self.interval
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((master_ip, master_port))
        self.socket.listen(max_clients)
        
    def run(self):
		while self.running:
			if time.time() >= self.next_update:
			    self.update.emit()
				self.next_update = time.time() + self.interval
			
			wait_time = self.next_update - time.time()
			
			wait_devs = [self.local_read] + self.master_clients.keys()
			
			try:
				rfds, wfds, efds = select.select(wait_devs, [], [], wait_time)
			
				for rfd in rfds:
					if rfd == self.socket:
						self.handle_connect()
                    else:
                        self.master_clients[rfd].handle()
						
			except select.error:
				pass
				
    def handle_connect(self, rfd):
        sock, address = self.socket.accept()
        self.master_clients[sock] = MasterClient(self, sock, address)

    def handle_disconnect(self, sock):
        del self.master_clients[sock]


