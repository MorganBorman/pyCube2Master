from Signals import SignalObject, Signal

from DatabaseManager import database_manager, Session
from sqlalchemy import or_
from sqlalchemy import Column, SmallInteger, Integer, BigInteger, String, Boolean, DateTime
from sqlalchemy import Sequence, ForeignKey
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relation, mapper, relationship, backref
from sqlalchemy.schema import UniqueConstraint

database_manager.initialize_tables()

class StatsModel(SignalObject):
    def __init__(self):
        SignalObject.__init__(self)
        
    def add_data(client, data):
        pass
