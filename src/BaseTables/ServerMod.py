from Common import *
from TableNames import table_names

class ServerMod(database_manager.Base):
    __tablename__ = table_names['ServerMod']
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    game_id         = Column(SmallInteger,     ForeignKey(table_names['Game']+'.id'),  nullable=False)
    name            = Column(String(32),    nullable=False)