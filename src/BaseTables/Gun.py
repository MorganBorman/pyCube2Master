from Common import *
from TableNames import table_names

class Gun(database_manager.Base):
    __tablename__ = table_names['Gun']
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    number          = Column(SmallInteger,  nullable=False, index=True)
    name            = Column(String(16),    nullable=False)
    damage          = Column(Integer,       nullable=False)