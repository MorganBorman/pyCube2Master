from Common import *
from TableNames import table_names

class FragEvent(database_manager.Base):
    __tablename__ = table_names['FragEvent']
    id = Column(BigInteger, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    who         = Column(BigInteger,    ForeignKey(table_names['User']+'.id'),     nullable=False)
    match_id    = Column(BigInteger,    ForeignKey(table_names['Match']+'.id'),    nullable=False)
    shot        = Column(BigInteger,    ForeignKey(table_names['ShotEvent']+'.id'),nullable=False)
    target      = Column(BigInteger,    ForeignKey(table_names['User']+'.id'),     nullable=True)
    
    when            = Column(DateTime,      nullable=False)
    type            = Column(SmallInteger,  nullable=False)