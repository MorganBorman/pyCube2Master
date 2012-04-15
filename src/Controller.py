from AuthenticationModel import AuthenticationModel
from ServersModel import ServersModel
from PunitiveModel import PunitiveModel
from StatsModel import StatsModel
from SocketView import SocketView

class Controller(object):
    def __init__(self, master_ip, master_port, max_clients):
    
        self.authentication_model = AuthenticationModel()
        self.servers_model = ServersModel()
        self.punitive_model = PunitiveModel()
        self.stats_model = StatsModel()
        self.socket_view = SocketView(master_ip, master_port, max_clients)
        
        
    def run(self):
        pass
