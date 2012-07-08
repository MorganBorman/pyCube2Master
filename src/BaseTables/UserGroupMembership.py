from Common import *
from TableNames import table_names

class UserGroupMembership(database_manager.Base):
    __tablename__ = table_names['UserGroupMembership']
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey(table_names['User']+'.id'), nullable=False)
    group_id = Column(Integer, ForeignKey(table_names['UserGroup']+'.id'), nullable=False)
    
    UniqueConstraint(user_id, group_id, name=__tablename__+'_uq_user_id_group_id')
    
    user = relationship('User', back_populates="group_memberships")
    group = relationship('UserGroup')
    
    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.name = group_id