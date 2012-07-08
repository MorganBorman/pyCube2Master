from Signals import SignalObject, Signal

import random
import cube2crypto

from BaseTables import User, UserName

class AuthenticationModel(SignalObject):

    challenge = Signal
    accept = Signal
    deny = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
        #key = (client, authid)
        #value = {'user': user, 'answer': answer}
        self.pending_auths = {}
        
        self.name_list = ""
        self.name_list_dirty = True
        
    def request_authentication(self, client, authid, email):
        
        user = User.by_email(email)
        
        if user is None:
            self.deny(authid)
            return
        
        pubkey = user.pubkey
        
        challenge, answer = cube2crypto.genchallenge(pubkey, format(random.getrandbits(128), 'X'))
        
        self.pending_auths[(client, authid)] = {'user': user, 'answer': answer}
        
        self.challenge.emit(client, authid, challenge)
        
    def confirm_authentication(self, client, authid, answer):
        
        if not (client, authid) in self.pending_auths.keys():
            self.deny.emait(client, authid)
            return
        
        pending_auth = self.pending_auths[(client, authid)]
        user = pending_auth['user']
        
        if answer != pending_auth['answer']:
            self.deny.emait(client, authid)
        else:
            self.accept.emit(client, 
                             authid, 
                             user.id, 
                             user.group_list,
                             user.name_list)
        
    def get_name_list(self):
        if self.name_list_dirty:
            name_list_list = []
            
            for name in UserName.all_names():
                name_list_list.append("na %s\n" % name)
                
            self.name_list = "".join(name_list_list)
            self.name_list_dirty = False
            
        return self.name_list


