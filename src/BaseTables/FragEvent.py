from Common import *
from TableNames import table_names

class FragEvent(database_manager.Base):
    __tablename__ = table_names['FragEvent']
    id = Column(BigInteger, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    who_id      = Column(BigInteger,    ForeignKey(table_names['User']+'.id'),     nullable=False)
    match_id    = Column(BigInteger,    ForeignKey(table_names['Match']+'.id'),    nullable=False)
    shot_id     = Column(BigInteger,    ForeignKey(table_names['ShotEvent']+'.id'),nullable=False)
    target_id   = Column(BigInteger,    ForeignKey(table_names['User']+'.id'),     nullable=True)
    
    when        = Column(DateTime,      nullable=False)
    type        = Column(SmallInteger,  nullable=False)
    
    types = enum(NORMAL=0, TEAMKILL=1, BOT=2, SPAWNKILL=3)
    
    who = relationship('User', primaryjoin="User.id==FragEvent.who_id")
    match = relationship('Match')
    shot = relationship('ShotEvent')
    target = relationship('User', primaryjoin="User.id==FragEvent.target_id")