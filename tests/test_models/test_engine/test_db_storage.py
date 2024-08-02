t DBStorage class
"""
import unittest
from models import storage
from models.state import State

class TestDBStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test class"""
        cls.storage = storage.all(State)
        cls.state = State(name="TestState")
        cls.state.save()

    def test_get(self):
        """Test the get method"""
        retrieved_state = storage.get(State, self.state.id)
        self.assertEqual(retrieved_state, self.state)
        self.assertIsNone(storage.get(State, "invalid_id"))

    def test_count(self):
        """Test the count method"""
        initial_count = storage.count(State)
        self.assertEqual(initial_count, 1)
        new_state = State(name="NewState")
        new_state.save()
        self.assertEqual(storage.count(State), 2)
        self.assertEqual(storage.count(), 2)  # Adjust based on the number of total objects

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        for obj in storage.all(State).values():
            storage.delete(obj)
        storage.save()

if __name__ == "__main__":
    unittest.main()

