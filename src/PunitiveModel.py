"""Clients only keep the current list of active effects."""

import time
from Signals import SignalObject, Signal

class PunitiveEffect(object):
    def __init__(self, effect_id, effect_type, target_id, target_ip, target_mask, target_name, master_id, master_ip, master_name, server_id, expiry, reason):
        self.effect_id = effect_id
        self.type = effect_type
        self.target_id = target_id
        self.target_ip = target_ip
        self.target_mask = target_mask
        self.target_name = target_name
        self.master_id = master_id
        self.master_ip = master_ip
        self.master_name = master_name
        self.server_id = server_id
        self.created_time = time.time()
        self.modified_time = time.time()
        self.expiry = self.expiry
        self.reason = reason

class PunitiveModel(SignalObject):

    update = Signal
    remove = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
        self.next_id = 0
        
        #key = effect_id
        #value = Effect
        self.effects = {}
        
        self.effect_list = ""
        self.effect_list_dirty = True
        
    def get_effect_id(self):
        try:
            return self.effect_id
        finally:
            self.effect_id += 1
        
    def create_effect(self, server, effect_type, target_id, target_name, target_ip, target_mask, master_id, master_name, master_ip, master_ip, reason):
        """Create an entry for a new specified punitive effect."""

        effect_id = self.get_effect_id()
        server_id = 0
        expiry = -1
        
        
        self.effects[effect_id] = PunitiveEffect(   effect_id, 
                                                    effect_type, 
                                                    target_id, 
                                                    target_name, 
                                                    target_ip, 
                                                    target_mask, 
                                                    master_id, 
                                                    master_name, 
                                                    master_ip, 
                                                    server_id, 
                                                    expiry, 
                                                    reason)
        
        self.effect_list_dirty = True
        self.update.emit(effect_id, effect_type, target_ip, target_mask, reason)
        
    def remove_effect(self, effect_id):
        if effect_id in self.effects.keys():
            del self.effects[effect_id]
            self.effect_list_dirty = True
            self.remove.emit(effect_id)
        
    def get_effect_list(self):
        if self.effect_list_dirty:
            effect_list_list = []
            
            for effect_id, effect in self.effects.items():
                effect_val = "ue %d %s %s %s %s\n" % (effect_id, effect.type, effect.target_ip, effect.target_mask, effect.reason)
                effect_list_list.append(effect_val)
            
            self.effect_list = "".join(effect_list_list)
            self.effect_list_dirty = False
        
        return self.effect_list
    
    def refresh(self):
        "Look for those effects which have expired and send out remove signals."
        pass
