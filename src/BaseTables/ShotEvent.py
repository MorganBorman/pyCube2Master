from Common import *
from TableNames import table_names

class ShotEvent(database_manager.Base):
    __tablename__ = table_names['ShotEvent']
    id = Column(BigInteger, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    match_id    = Column(BigInteger,    ForeignKey(table_names['Match']+'.id'),    nullable=False)
    who         = Column(BigInteger,    ForeignKey(table_names['User']+'.id'),     nullable=False)
    gun         = Column(SmallInteger,  ForeignKey(table_names['Gun']+'.id'),      nullable=False)
    
    when = Column(DateTime, nullable=False)