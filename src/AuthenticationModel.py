from Signals import SignalObject, Signal

class AuthenticationModel(SignalObject):
    
    authenticate = Signal
    challenge = Signal
    deny = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
    def request_authentication(self, authid, name):
        pass
        
    def confirm_authentication(self, authid, answer):
        pass
        
    
