from Common import *
from TableNames import table_names

class ServerInstance(database_manager.Base):
    __tablename__ = table_names['ServerInstance']
    id        = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    domain_id       = Column(SmallInteger,      ForeignKey(table_names['ServerDomain']+'.id'),      nullable=False)
    game_id         = Column(SmallInteger,      ForeignKey(table_names['Game']+'.id'),              nullable=False)
    mod_id          = Column(SmallInteger,      ForeignKey(table_names['ServerMod']+'.id'),         nullable=False)
    
    name            = Column(String(32),        nullable=False)
    port            = Column(Integer,           nullable=False)
    
    