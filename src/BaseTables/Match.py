from Common import *
from TableNames import table_names

class Match(database_manager.Base):
    __tablename__ = table_names['Match']
    id = Column(BigInteger, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    mode_id         = Column(SmallInteger,      ForeignKey(table_names['Mode']+'.id'),              nullable=False)
    pseudomode_id   = Column(SmallInteger,      ForeignKey(table_names['PseudoMode']+'.id'),        nullable=False)
    server_id       = Column(Integer,           ForeignKey(table_names['ServerInstance']+'.id'),    nullable=False)
    game_version_id = Column(Integer,           ForeignKey(table_names['GameVersion']+'.id'),       nullable=False)
    
    start           = Column(DateTime,          nullable=False)
    end             = Column(DateTime,          nullable=False)