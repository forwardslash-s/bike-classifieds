from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    """Registered user information stored in database"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'name': self.name,
           'id': self.id,
           'email': self.email,
           }


class Model(Base):
    """Defines the Categories of Bikes"""
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'name': self.name,
           'id': self.id,
        }


class Bike(Base):
    """Table for individual listings"""
    __tablename__ = 'bike'

    name = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    type_id = Column(Integer, ForeignKey('model.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    model = relationship('Model', backref=backref(
        "Model", cascade="all, delete-orphan"))
    user = relationship('User')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id': self.id,
           'name': self.name,
           'description': self.description,
           'price': self.price,
           'type_id': self.type_id,
           'user_id': self.user_id,
           }


engine = create_engine('sqlite:///bikecatalog.db')
Base.metadata.create_all(engine)
