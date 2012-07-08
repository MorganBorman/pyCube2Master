from Common import *
from TableNames import table_names

class UserName(database_manager.Base):
    __tablename__ = table_names['UserName']
    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)
    user_id = Column(BigInteger,        ForeignKey(table_names['User']+'.id'),      nullable=False)
    name    = Column(String(16), nullable=False)
    
    UniqueConstraint(name, name=__tablename__+'_uq_name')
    
    user = relationship('User', back_populates="names")
    
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        
    @staticmethod
    def all_names():
        with Session() as session:
            return session.query(UserName.name).all()