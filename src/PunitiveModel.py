"""Clients only keep the current list of active effects."""

import datetime
from Signals import SignalObject, Signal

from DatabaseManager import database_manager, Session
from sqlalchemy import or_
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime
from sqlalchemy import Sequence, ForeignKey
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relation, mapper, relationship, backref
from sqlalchemy.schema import UniqueConstraint

from AuthenticationModel import User

NEVEREXPIRES = -1
EXPIRYDATE = 0




        
database_manager.initialize_tables()

class PunitiveModel(SignalObject):

    update = Signal
    remove = Signal

    def __init__(self):
        SignalObject.__init__(self)
        
        self.effect_list = ""
        self.effect_list_dirty = True
        
    def create_effect(self, server, effect_type_name, target_id, target_name, target_ip, target_mask, 
                      master_id, master_name, master_ip, reason):
        """Create an entry for a new specified punitive effect."""
        
        effect_type = EffectType.by_name(effect_type_name)
        
        if effect_type is None:
            return
        
        self.effects[effect_id] = PunitiveEffect(   effect_type, 
                                                    target_id, 
                                                    target_name, 
                                                    target_ip, 
                                                    target_mask, 
                                                    master_id, 
                                                    master_name, 
                                                    master_ip, 
                                                    reason)
        
        self.effect_list_dirty = True
        self.update.emit(effect_id, effect_type.name, target_ip, target_mask, reason)
        
    def remove_effect(self, effect_id):
        if PunitiveEffect.expire(effect_id):
            self.effect_list_dirty = True
            self.remove.emit(effect_id)
        
    def get_effect_list(self):
        if self.effect_list_dirty:
            effect_list_list = []
            
            with Session() as session:
                punitive_effect_query = session.query(PunitiveEffect.id, PunitiveEffect.effect_type.name, PunitiveEffect.target_ip, PunitiveEffect.target_mask, PunitiveEffect.reason)
                rows = punitive_effect_query.filter(not PunitiveEffect.expired).all()
            
                for effect_id, effect_type, target_ip, target_mask, reason in rows:
                    effect_val = "ue %ld %s %ld %ld %s\n" % (effect_id, effect.type, target_ip, target_mask, reason)
                    effect_list_list.append(effect_val)
            
            self.effect_list = "".join(effect_list_list)
            self.effect_list_dirty = False
        
        return self.effect_list
    
    def refresh(self):
        "Look for those effects which have expired and send out remove signals."
        with Session() as session:
            punitive_effect_query = session.query(PunitiveEffect)
            punitive_effect_query = PunitiveEffect.expired(punitive_effect_query)
            
            expired_punitive_effects = punitive_effect_query.all()
            
            for punitive_effect in expired_punitive_effects:
                punitive_effect.expired = True
                self.remove.emit(punitive_effect.id)
                
            session.commit()
