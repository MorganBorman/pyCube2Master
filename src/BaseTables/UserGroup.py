from Common import *
from TableNames import table_names

class UserGroup(database_manager.Base):
    __tablename__ = table_names['UserGroup']
    id = Column(Integer, Sequence(__tablename__+'_id_seq'), primary_key=True)
    name = Column(String(48), nullable=False)
    
    def __init__(self, name):
        self.name = name