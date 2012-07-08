import CategoryConfig, sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

def get_database_uri():
    config_path = "../"
    config_category = "database"
    config_extension = ".conf"
    
    config_object = CategoryConfig.CategoryConfig(config_path, config_category, config_extension)
    
    #place the database by default in the instances directory
    default_db_path = "sqlite:///../pyCube2Master.db"
    
    doc = 'Sqlalchemy uri string indicating the database connection parameters.'
    return config_object.getOption('database.uri', default_db_path, doc)


class DatabaseManager():
    def __init__(self):
        self.is_connected = False
        self.uri = get_database_uri()
        self.engine = None
        self.session_factory = None
        self.Base = declarative_base()
        
    def connect(self):
        if not self.is_connected:
            self.engine = sqlalchemy.create_engine(self.uri)
            self.session_factory = sqlalchemy.orm.sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
            self.is_connected = True
            
    def initialize_tables(self):
        self.connect()
        self.Base.metadata.create_all(self.engine)
    
    def get_session(self):
        try:
            self.engine.execute("SELECT 1;")
        except:
            del self.session_factory
            del self.engine
            self.is_connected = False
            self.connect()

        return self.session_factory()
        
database_manager = DatabaseManager()

@contextmanager
def Session():
    session = database_manager.get_session()
    try:
        yield session
    finally:
        session.close()