from Common import *
from TableNames import table_names

class CaptureEvent(database_manager.Base):
    __tablename__ = table_names['CaptureEvent']
    id = Column(BigInteger, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    match_id    = Column(BigInteger,    ForeignKey(table_names['Match']+'.id'),    nullable=False)
    who         = Column(BigInteger,    ForeignKey(table_names['User']+'.id'),     nullable=False)
    
    start       = Column(DateTime,      nullable=False)
    end         = Column(DateTime,      nullable=False)
    team        = Column(SmallInteger,  nullable=True)
    complete    = Column(Boolean,       nullable=False)
    health      = Column(Integer,       nullable=False)