from Common import *
from TableNames import table_names

class DeathEvent(database_manager.Base):
    __tablename__ = table_names['DeathEvent']
    id = Column(BigInteger, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    who         = Column(BigInteger,    ForeignKey(table_names['User']+'.id'),     nullable=False)
    match_id    = Column(BigInteger,    ForeignKey(table_names['Match']+'.id'),    nullable=False)
    killer      = Column(BigInteger,    ForeignKey(table_names['User']+'.id'),     nullable=True)
    shot        = Column(BigInteger,    ForeignKey(table_names['ShotEvent']+'.id'),nullable=True)
    
    when        = Column(DateTime,      nullable=False)
    type        = Column(SmallInteger,  nullable=False)