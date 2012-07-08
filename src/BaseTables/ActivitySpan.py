from Common import *
from TableNames import table_names

class ActivitySpan(database_manager.Base):
    __tablename__ = table_names['ActivitySpan']
    id = Column(BigInteger, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    who     = Column(BigInteger,        ForeignKey(table_names['User']+'.id'),      nullable=False)
    
    type    = Column(SmallInteger,      nullable=False)
    start   = Column(DateTime,          nullable=False)
    end     = Column(DateTime,          nullable=False)
    millis  = Column(Integer,           nullable=False)