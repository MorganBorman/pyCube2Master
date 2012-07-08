from Common import *
from TableNames import table_names

class User(database_manager.Base):
    __tablename__ = table_names['User']
    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)
    email = Column(String(128), index=True)
    pubkey = Column(String(49), nullable=False)
    approved = Column(Boolean)
    
    UniqueConstraint(email, name=__tablename__+'_uq_email')
    
    names = relationship("UserName", order_by="UserName.id", backref="user")
    groups = relationship("UserGroupMembership", order_by="UserGroupMembership.id", backref="user")
    
    def __init__(self, email, pubkey):
        self.email = email
        self.pubkey = pubkey
        self.approved = True
        
    @property
    def name_list(self):
        with Session() as session:
            return session.query(UserName.name).filter(UserName.user_id==self.id).all()
        
    @property
    def group_list(self):
        with Session() as session:
            return session.query(UserGroupMembership.group.name).filter(UserGroupMembership.user_id==self.id).all()
        
    @staticmethod
    def by_email(email):
        try:
            with Session() as session:
                return session.query(User).filter(User.email==email).one()
        except NoResultFound:
            return None