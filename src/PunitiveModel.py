"""Clients only keep the current list of active effects."""

from Signals import SignalObject, Signal

class PunitiveModel(SignalObject):

    update = Signal
    remove = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
    def update_effect(self, effect_type, target_ip, target_mask, reason, master_ip, master_name, server_domain, expiry):
        """Update an entry for a specified punitive effect. 
        
        (effect_type, target_ip, target_mask) can be considered a primary key.
        
        If no active effect for the key specified parameters exists a new one will be created.
        
        If expiry is set to -1 the effect will be disabled.
        """
        pass
        
    def get_effect_list(self):
        pass
