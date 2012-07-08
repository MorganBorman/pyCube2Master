"""Represents the body of the server list data."""

from Signals import SignalObject, Signal
import time
import cube2crypto
import random

from DatabaseManager import database_manager, Session
from sqlalchemy import or_
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime
from sqlalchemy import Sequence, ForeignKey
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relation, mapper, relationship, backref
from sqlalchemy.schema import UniqueConstraint


        
database_manager.initialize_tables()

class ServersModel(SignalObject):

    challenge = Signal
    accept = Signal
    deny = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
        self.server_list = ""
        self.server_list_dirty = True
        
        #key = client
        #value = (port, time, server_domain, answer)
        self.servers_pending = {}
        
        #key = client
        #value = (port, time, server_domain)
        self.servers = {}
        
    def register_server(self, client, server_domain, port):
        "Attempt to register a newly connected server."
        
        if client in self.servers.keys():
            self.servers[client]['time'] = time.time()
            return
        
        server = Server.by_domain(server_domain)
        
        if server is None:
            self.deny.emit(client)
            return
        
        pubkey = server.pubkey
        
        challenge, answer = cube2crypto.genchallenge(pubkey, format(random.getrandbits(128), 'X'))
        
        self.servers_pending[client] = {'port': port, 'time': time.time(), 'server_domain': server_domain, 'answer': answer}
        
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
        self.server_list_dirty = True
        self.accept.emit(client)
        
    def is_server_confirmed(self, client):
        "Check whether the specified server has been confirmed."
        return client in self.servers.keys()
        
    def remove_server(self, client):
        "Removed the specified server from the list."
        if client in self.servers.keys():
            del self.servers[client]
            self.server_list_dirty = True
            
        if client in self.servers_pending.keys():
            del self.servers_pending[client]
        
    def refresh(self):
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

