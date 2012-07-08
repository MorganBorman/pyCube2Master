from Common import *
from TableNames import table_names

class Mode(database_manager.Base):
    __tablename__ = table_names['Mode']
    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)
    
    game_id         = Column(SmallInteger,      ForeignKey(table_names['Game']+'.id'),  nullable=False)
    
    number          = Column(SmallInteger,      nullable=False)
    name            = Column(String(16),        nullable=False)