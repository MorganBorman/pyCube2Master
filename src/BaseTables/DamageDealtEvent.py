from Common import *
from TableNames import table_names

class DamageDealtEvent(database_manager.Base):
    __tablename__ = table_names['DamageDealtEvent']
    id = Column(BigInteger, Sequence(__tablename__ + '_id_seq'), primary_key=True)
    
    match_id    = Column(BigInteger,    ForeignKey(table_names['Match']+'.id'),    nullable=False)
    target      = Column(BigInteger,    ForeignKey(table_names['User']+'.id'),     nullable=False)
    shot        = Column(BigInteger,    ForeignKey(table_names['ShotEvent']+'.id'),nullable=False)
    
    when        = Column(DateTime,      nullable=False)
    distance    = Column(Integer,       nullable=False)