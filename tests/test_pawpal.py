import unittest
from pawpal_system import Task, Pet, TaskFrequency


class TestTaskCompletion(unittest.TestCase):
    """Test task completion functionality"""

    def setUp(self):
        """Create a test task before each test"""
        self.task = Task(
            id="test_task_001",
            description="Test walk",
            category="walk",
            duration_minutes=30,
            frequency=TaskFrequency.DAILY,
            priority="high"
        )

    def test_task_initially_incomplete(self):
        """Verify task starts as incomplete"""
        self.assertFalse(self.task.is_completed)

    def test_mark_completed_changes_status(self):
        """Verify that calling mark_completed() changes task's status to True"""
        self.task.mark_completed()
        self.assertTrue(self.task.is_completed)

    def test_mark_incomplete_changes_status(self):
        """Verify that calling mark_incomplete() changes task's status to False"""
        self.task.mark_completed()
        self.assertTrue(self.task.is_completed)
        self.task.mark_incomplete()
        self.assertFalse(self.task.is_completed)


class TestTaskAddition(unittest.TestCase):
    """Test adding tasks to pets"""

    def setUp(self):
        """Create a test pet and task before each test"""
        self.pet = Pet(
            id="test_pet_001",
            name="Buddy",
            species="Dog",
            breed="Labrador",
            age=2
        )
        self.task = Task(
            id="test_task_002",
            description="Test feed",
            category="feed",
            duration_minutes=10,
            frequency=TaskFrequency.DAILY,
            priority="high"
        )

    def test_pet_starts_with_no_tasks(self):
        """Verify pet starts with empty task list"""
        self.assertEqual(len(self.pet.tasks), 0)

    def test_adding_task_increases_count(self):
        """Verify that adding a task to a Pet increases task count"""
        initial_count = len(self.pet.tasks)
        self.pet.add_task(self.task)
        new_count = len(self.pet.tasks)
        self.assertEqual(new_count, initial_count + 1)

    def test_adding_multiple_tasks(self):
        """Verify that adding multiple tasks increases count correctly"""
        task2 = Task(
            id="test_task_003",
            description="Test play",
            category="enrichment",
            duration_minutes=20,
            frequency=TaskFrequency.DAILY,
            priority="medium"
        )
        self.pet.add_task(self.task)
        self.pet.add_task(task2)
        self.assertEqual(len(self.pet.tasks), 2)

    def test_added_task_is_retrievable(self):
        """Verify that an added task can be retrieved"""
        self.pet.add_task(self.task)
        retrieved_task = self.pet.get_task(self.task.id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.id, self.task.id)
        self.assertEqual(retrieved_task.description, "Test feed")


if __name__ == "__main__":
    unittest.main()
