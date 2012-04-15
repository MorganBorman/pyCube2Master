"""Represents the body of the server list data."""

from Signals import SignalObject, Signal
import time

class ServersModel(SignalObject):

    authenticate = Signal
    challenge = Signal
    deny = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
        #key = (server_ip, server_port)
        #value = (time, server_domain, answer)
        self.servers_pending = {}
        
        #key = (server_ip, server_port)
        #value = (time, server_domain)
        self.servers = {}
        
    def connect_server(self, server_ip, server_port, server_domain):
        "Attempt to authenticate a newly connected server."
        pass
        
    def confirm_server(self, server_ip, server_port, answer):
        "Confirm a connected servers authentication."
        pass
        
    def is_server_confirmed(self, server_ip, server_port):
        "Check whether the specified server has been confirmed."
        
    def refresh_server(self, server_ip, server_port):
        "Refresh the last seen entry for the specified server."
        pass
        
    def remove_server(self, server_ip, server_port):
        "Removed the specified server from the list."
        pass
        
    def clean(self):
        "Look for servers which have timed out."
        pass
        
    def get_server_list(self):
        "Get the current list of servers."
        pass
