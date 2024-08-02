torage engine using JSON file.
"""
import json
from models.base_model import BaseModel
from models import base_model
from models import state
from models import city
from models import user
import os

class FileStorage:
    """FileStorage class for JSON file storage"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of all objects in storage"""
        if cls:
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """Add a new object to the storage"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Save all objects to a JSON file"""
        with open(self.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """Load all objects from the JSON file"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as f:
                objects = json.load(f)
                for key, value in objects.items():
                    class_name = value['__class__']
                    cls = getattr(base_model, class_name, None)
                    if cls:
                        self.__objects[key] = cls(**value)

    def get(self, cls, id):
        """Retrieve an object by class and ID"""
        if cls.__name__ not in self.__objects:
            return None
        return self.__objects.get(f"{cls.__name__}.{id}")

    def count(self, cls=None):
        """Count the number of objects in storage for a class or all objects"""
        if cls:
            return len([obj for obj in self.__objects.values() if isinstance(obj, cls)])
        return len(self.__objects)

