from Common import *
from TableNames import table_names

class ServerInstance(database_manager.Base):
    __tablename__ = table_names['ServerInstance']
    id        = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    
    domain_id       = Column(SmallInteger,      ForeignKey(table_names['ServerDomain']+'.id'),      nullable=False)
    game_id         = Column(SmallInteger,      ForeignKey(table_names['Game']+'.id'),              nullable=False)
    mod_id          = Column(SmallInteger,      ForeignKey(table_names['ServerMod']+'.id'),         nullable=False)
    
    name            = Column(String(32),        nullable=False)
    port            = Column(Integer,           nullable=False)
    
    domain  = relationship('ServerDomain',  backref=backref('instances',        order_by=id))
    game    = relationship('Game',          backref=backref('server_instances', order_by=id))
    mod     = relationship('ServerMod',     backref=backref('server_instances', order_by=id))
    
    @staticmethod
    def by_domain_port(domain, port):
        with Session() as session:
            try:
                return session.query(ServerInstance).filter(ServerInstance.domain.name==domain).filter(ServerInstance.port==port).one()
            except NoResultFound:
                return None