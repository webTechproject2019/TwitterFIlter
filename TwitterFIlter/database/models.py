from sqlalchemy import Integer, Column, String, DateTime

from sqlalchemy.sql import func
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


class User(Base):
    __tablename__ = 'User'
    user_id = Column(String(20), primary_key=True, autoincrement="auto")
    name = Column(String(20), unique=True)
    screen_name = Column(String(20), unique=True)
    location = Column(String(20), unique=True)

    def __init__(self,user_id, name, screen_name,location = None):
           self.user_id=user_id
           self.name = name
           self.screen_name=screen_name
           self.location = location

    def toDict(self):
         return {
            'user_id': self.user_id,
            'name': self.name,
            'screen_name': self.screen_name,
            'location': self.location
        }

class Tweets(Base):
    __tablename__ = 'tweets'
    created_at= Column(String(50), unique=True)
    id = Column(String(50), primary_key=True, autoincrement="auto")
    id_str = Column(String(50), unique=True)
    text= Column(String(50), unique=True)
    user = Column(String(50), unique=True)
    place= Column(String(50), unique=True)
    entities = Column(String(50), unique=True)

    def __init__(self,created_at,id,id_str, text, user,place,entities):
           self.created_at=created_at
           self.id= id
           self.id_str=id_str
           self.text= text
           self.user=user
           self.place=place
           self.entities=entities


    def toDict(self):
         return {
            'created_at': self.created_at,
            'id': self.id,
            'id_str': self.id_str,
            'text': self.text,
            'user':self.user,
            'place':self.place,
            'entities':self.entities

        }                       
            
