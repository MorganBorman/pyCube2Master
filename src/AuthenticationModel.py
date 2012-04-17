from Signals import SignalObject, Signal

import random
import cube2crypto

class User(object):
    def __init__(self, email, pubkey, groups, names):
        self.email = email
        self.pubkey = pubkey
        self.groups = groups
        self.names = names

class AuthenticationModel(SignalObject):

    challenge = Signal
    accept = Signal
    deny = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
        #key = email
        #value = User
        self.users = {}
        self.users['fd.chasm@gmail.com'] = User('fd.chasm@gmail.com', '+eb7065c2976a8f4f26e179eb0ed4af4b2eb27c157f918c85', ['admin', 'clan', 'coleader'], ['chasm'])
        
        #key = (client, authid)
        #value = answer
        self.pending_auths = {}
        
        self.name_list = ""
        self.name_list_dirty = True
        
    def request_authentication(self, client, authid, email):
        
        if not email in self.users.keys():
            self.deny(authid)
            return
        
        pubkey = self.users[email].pubkey
        
        challenge, answer = cube2crypto.genchallenge(pubkey, format(random.getrandbits(128), 'X'))
        
        self.pending_auths[(client, authid)] = {'user': self.users[email], 'answer': answer}
        
        self.challenge.emit(client, authid, challenge)
        
    def confirm_authentication(self, client, authid, answer):
        
        if not (client, authid) in self.pending_auths.keys():
            self.deny.emait(client, authid)
            return
        
        pending_auth = self.pending_auths[(client, authid)]
        
        if answer != pending_auth['answer']:
            self.deny.emait(client, authid)
            return
        
        self.accept.emit(client, authid, pending_auth['user'].groups, pending_auth['user'].names)
        
    def get_name_list(self):
        if self.name_list_dirty:
            name_list_list = []
            
            for user in self.users.values():
                for name in user.names:
                    name_list_list.append("na %s\n" % name)
                
            self.name_list = "".join(name_list_list)
            self.name_list_dirty = False
            
        return self.name_list


