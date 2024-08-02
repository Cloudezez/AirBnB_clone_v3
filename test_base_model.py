t cases for BaseModel
"""
import unittest
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    def test_initialization(self):
        """Test the initialization of BaseModel."""
        obj = BaseModel()
        self.assertIsInstance(obj, BaseModel)

if __name__ == '__main__':
    unittest.main()

