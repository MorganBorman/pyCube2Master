"""Represents the body of the ban, mute, and spec data."""

from Signals import SignalObject, Signal

class PunitiveModel(SignalObject):

    update = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
    def update_effect(self, target_ip, target_mask, reason, master_ip, master_name, server_domain):
        pass
        
    def get_effect_list(self):
        pass
