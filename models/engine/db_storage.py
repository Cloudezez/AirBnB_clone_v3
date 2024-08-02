tabase Storage engine using SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models import base_model
import os

class DBStorage:
    """DBStorage class for SQLAlchemy database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Create the engine and bind it to the session"""
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}')
        Base.metadata.create_all(self.__engine)
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def all(self, cls=None):
        """Query all objects based on the class name"""
        objects = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        else:
            for cls in Base.__subclasses__():
                for obj in self.__session.query(cls).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add a new object to the session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload all objects from the database"""
        self.__session.remove()
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def get(self, cls, id):
        """Retrieve an object by class and ID"""
        if cls not in Base.__subclasses__():
            return None
        return self.__session.query(cls).get(id)

    def count(self, cls=None):
        """Count the number of objects in storage for a class or all objects"""
        if cls:
            if cls not in Base.__subclasses__():
                return 0
            return self.__session.query(cls).count()
        count = 0
        for cls in Base.__subclasses__():
            count += self.__session.query(cls).count()
        return count

