from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, DateTime

engine = create_engine('sqlite:///webTech.db')
#from pdb import set_trace;set_trace()

maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
b_session = scoped_session(maker)

#session=sessionmaker(bind=engine)()

# The Base is the class that will be used to create Models
# The SQLAlchemy ORM Models will extend this class
Base = declarative_base()
#Base.query = db_session.query_property()


def init_db():
    # Import all the classes that will be used to create ORM Models
    from models import User
    from models import Tweets
    Base.metadata.create_all(bind=engine)

# class User(Base):
#     __tablename__ = 'User'
#     user_id = Column(String(20), primary_key=True)
#     name = Column(String(20), unique=True)
#     screen_name = Column(String(20), unique=True)
#     location = Column(String(20), unique=True)

#     def __init__(self,user_id, name, screen_name,location = None):
#            self.user_id=user_id
#            self.name = name
#            self.screen_name=screen_name
#            self.location = location

# User=User("5","akeem","@akeem","trindad")    
# session.add(User)     
# session.commit()
