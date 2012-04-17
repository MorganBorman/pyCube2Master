from AuthenticationModel import AuthenticationModel
from ServersModel import ServersModel
from PunitiveModel import PunitiveModel
from StatsModel import StatsModel
from SocketManager import SocketManager

class Controller(object):
    def __init__(self, master_ip, master_port, max_clients):
    
        self.authentication_model = AuthenticationModel()
        self.servers_model = ServersModel()
        self.punitive_model = PunitiveModel()
        self.stats_model = StatsModel()
        self.socket_manager = SocketManager(master_ip, master_port, max_clients)
        
        #######################################
        #connect up our signals
        #######################################
        
        #SocketManager
        
        self.socket_manager.started.connect(self.on_started)
        self.socket_manager.stopped.connect(self.on_stopped)
        self.socket_manager.connect.connect(self.on_connect)
        self.socket_manager.request.connect(self.on_request)
        self.socket_manager.disconnect.connect(self.on_disconnect)
        
        #ServersModel
        
        self.servers_model.challenge.connect(self.on_challenge)
        self.servers_model.accept.connect(self.on_accept)
        self.servers_model.deny.connect(self.on_deny)
        
        #AuthenticationModel
        
        self.authentication_model.challenge.connect(self.on_auth_challenge)
        self.authentication_model.accept.connect(self.on_auth_accept)
        self.authentication_model.deny.connect(self.on_auth_deny)
        
        #######################################
        #start up the socket_manager
        #######################################
        
        self.socket_manager.run()
        
    def on_started(self, ip, port):
        print "Master server started."
        print "Listening on (%s, %s)." %(str(ip), str(port))
        print "Press Ctrl-c to exit."
        
    def on_stopped(self):
        print "\nMaster server stopped."
        
    def on_connect(self, client):
        print "client connected %s" % str(client.address)
    
    def on_request(self, client, data):
        print "client request %s:" % str(client.address), data
        
        """
        #inbound messages
        
        list = list servers
        sr = server registration
        sc = server confirmation
        
        ar = authentication request
        ac = authentication confirmation
        
        eu = effect update
        er = effect remove
        
        su = update stats
        
        #outbound messages
        
        rc = registration challenge
        rs = registration success
        rf = registration failure
        
        ac = authentication challenge
        as = authentication success
        af = authentication failure
        
        na = names add
        nr = names remove
        
        eu = effect update
        er = effect remove
        """
        
        if data[0] == "list":
            list = self.servers_model.get_server_list()
            client.send(list)
        if data[0] == "sr":
            self.servers_model.register_server(client, data[1], data[2])
        elif data[0] == "sc":
            self.servers_model.confirm_server(client, data[1])
        elif not self.servers_model.is_server_confirmed(client):
            client.disconnect()
            return
        
        if data[0] == "ar":
            self.authentication_model.request_authentication(client, data[1], data[2])
        elif data[0] == "ac":
            self.authentication_model.confirm_authentication(client, data[1], data[2])
        elif data[0] == "eu":
            pass
        elif data[0] == "su":
            user = data[1]
    
    def on_disconnect(self, client):
        print "client disconnected %s" % str(client.address)
        
    def on_challenge(self, client, challenge):
        message = "rc %s\n" % challenge
        client.send(message)
    
    def on_accept(self, client):
        client.unlimit()
        effect_list = self.punitive_model.get_effect_list()
        names_list = self.authentication_model.get_name_list()
        message = "".join(("rs\n", effect_list, names_list))
        client.send(message)
    
    def on_deny(self, client):
        client.send("rf\n")
        client.disconnect()
        
    def on_auth_challenge(self, client, authid, challenge):
        message = "ac %s %s\n" % (authid, challenge)
        client.send(message)
    
    def on_auth_accept(self, client, authid, groups, names):
        message = "as %s %s %s\n" % (authid, ','.join(groups), ','.join(names))
        client.send(message)
    
    def on_auth_deny(self, client, authid):
        message = "af %s\n" % authid
        client.send(message)
        