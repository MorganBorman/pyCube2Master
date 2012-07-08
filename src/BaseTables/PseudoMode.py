from Common import *
from TableNames import table_names

class PseudoMode(database_manager.Base):
    __tablename__ = table_names['PseudoMode']
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    mod_id          = Column(Integer,     ForeignKey(table_names['ServerMod']+'.id'),       nullable=False)
    
    name            = Column(String(32),    nullable=False)
    number          = Column(SmallInteger,  nullable=False)