from Common import *
from TableNames import table_names

class ServerDomain(database_manager.Base):
    __tablename__ = table_names['ServerDomain']
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    domain = Column(String(64), index=True)
    pubkey = Column(String(49))
    
    UniqueConstraint(domain, name=__tablename__+'_uq_domain')
    
    def __init__(self, domain, pubkey):
        self.domain = domain
        self.pubkey = pubkey