from Common import *
from TableNames import table_names

class Game(database_manager.Base):
    __tablename__ = table_names['Game']
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    name            = Column(String(32),    nullable=False)