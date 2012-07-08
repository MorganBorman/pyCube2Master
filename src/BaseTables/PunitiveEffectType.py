from Common import *
from TableNames import table_names

class PunitiveEffectType(database_manager.Base):
    __tablename__ = table_names['PunitiveEffectType']
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    name = Column(String(16))
    default_expiry_type = Column(Integer)
    default_duration = Column(BigInteger)
    
    expiry_types = enum(NEVEREXPIRES=-1, EXPIRYDATE=0)
    
    UniqueConstraint(name, name=__tablename__+'_uq_name')
    
    def __init__(self, name, default_expiry_type, default_duration):
        self.name = name
        self.default_expiry_type = default_expiry_type
        self.default_duration = default_duration
        
    @staticmethod
    def by_name(name):
        try:
            with Session() as session:
                return session.query(EffectType).filter(PunitiveEffectType.name==name).one()
        except NoResultFound:
            return None