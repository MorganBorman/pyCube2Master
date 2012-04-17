"""Clients only keep the current list of active effects."""

from Signals import SignalObject, Signal

class PunitiveEffect(object):
    def __init__(self, effect_type, target_ip, target_mask, reason, master_ip, master_name, server_domain, expiry):
        self.type = effect_type
        self.target_ip = target_ip
        self.target_mask = target_mask
        self.reason = reason
        self.master_ip = master_ip
        self.master_name = master_name
        self.server_domain = server_domain
        self.expiry = self.expiry

class PunitiveModel(SignalObject):

    update = Signal
    remove = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
        #key = (effect_type, target_ip, target_mask)
        #value = Effect
        self.effects = {}
        
        self.effect_list = ""
        self.effect_list_dirty = True
        
    def update_effect(self, effect_type, target_ip, target_mask, reason, master_ip, master_name, server_domain, expiry):
        """Update an entry for a specified punitive effect. 
        
        (effect_type, target_ip, target_mask) can be considered a primary key.
        
        If no active effect for the key specified parameters exists a new one will be created.
        """
        if (effect_type, target_ip, target_mask) in self.effects.keys():
            pass
        else:
            effect = PunitiveEffect(effect_type, target_ip, target_mask, reason, master_ip, master_name, server_domain, expiry)
            self.effects[(effect_type, target_ip, target_mask)] = effect
        
        self.effect_list_dirty = True
        self.update.emit(effect_type, target_ip, target_mask, reason)
        
    def remove_effect(self, effect_type, target_ip, target_mask):
        if (effect_type, target_ip, target_mask) in self.effects.keys():
            del self.effects[(effect_type, target_ip, target_mask)]
            self.effect_list_dirty = True
            self.remove.emit(effect_type, target_ip, target_mask)
        
    def get_effect_list(self):
        if self.effect_list_dirty:
            effect_list_list = []
            
            for effect in self.effects.values():
                effect_val = "ue %s %s %s %s\n" % (effect.type, effect.target_ip, effect.target_mask, effect.reason)
                effect_list_list.append(effect_val)
            
            self.effect_list = "".join(effect_list_list)
            self.effect_list_dirty = False
        
        return self.effect_list
    
    def refresh(self):
        "Look for those effects which have expired and send out remove signals."
        pass
