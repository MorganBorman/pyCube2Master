from Common import *
from TableNames import table_names

class ServerDomain(database_manager.Base):
    __tablename__ = table_names['ServerDomain']
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    name = Column(String(64), index=True)
    pubkey = Column(String(49))
    
    UniqueConstraint(name, name=__tablename__+'_uq_name')
    
    def __init__(self, name, pubkey):
        self.name = name
        self.pubkey = pubkey
        
    @staticmethod
    def by_domain(domain):
        with Session() as session:
            try:
                return session.query(ServerDomain).filter(ServerDomain.name==domain).one()
            except NoResultFound:
                return None