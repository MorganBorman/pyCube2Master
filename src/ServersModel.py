"""Represents the body of the server list data."""

from Signals import SignalObject, Signal
import time
import cube2crypto
import random

class ServersModel(SignalObject):

    challenge = Signal
    accept = Signal
    deny = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
        self.server_list = ""
        self.server_list_dirty = True
        
        self.valid_servers = {}
        self.valid_servers['example.com'] = "-059f164dff16e859fc5c00a82e6d5f2ae0b36a441b29edf5"
        
        #key = client
        #value = (port, time, server_domain, answer)
        self.servers_pending = {}
        
        #key = client
        #value = (port, time, server_domain)
        self.servers = {}
        
    def register_server(self, client, server_domain, port):
        "Attempt to register a newly connected server."
        if not server_domain in self.valid_servers.keys():
            self.deny.emit(client)
            return
        
        pubkey = self.valid_servers[server_domain]
        
        challenge, answer = cube2crypto.genchallenge(pubkey, format(random.getrandbits(128), 'X'))
        
        self.servers_pending[client] = {'port': port, 'time': time, 'server_domain': server_domain, 'answer': answer}
        
        self.challenge.emit(client, challenge)
        
    def confirm_server(self, client, answer):
        "Confirm a connected servers authentication."
        if not client in self.servers_pending.keys():
            self.deny.emit(client)
            return
        
        data = self.servers_pending[client]
        del self.servers_pending[client]
        
        if data['answer'] != answer:
            self.deny.emit(client)
            return
        
        del data['answer']
        
        self.servers[client] = data
        
        self.accept.emit(client)
        
    def is_server_confirmed(self, client):
        "Check whether the specified server has been confirmed."
        return client in self.servers.keys()
        
    def remove_server(self, client):
        "Removed the specified server from the list."
        if client in self.servers.keys():
            del self.servers[client]
            
        if client in self.servers_pending.keys():
            del self.servers_pending[client]
        
    def clean(self):
        "Look for servers which have timed out."
        pass
        
    def get_server_list(self):
        "Get the current list of servers."
        if self.server_list_dirty:
            server_list_list = []
            for client, data in self.servers.items():
                server_ip = client.address[0]
                server_port = data['port']
                server_list_list.append("addserver %s %s\n" %(server_ip, server_port))
            self.server_list = "".join(server_list_list)
            self.server_list_dirty = False
            
        return self.server_list
        
    def broadcast(self, data):
        "Send a message to all confirmed servers."
        for client in self.servers.keys():
            client.send(data)

