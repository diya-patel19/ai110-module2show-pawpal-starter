import unittest
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))
from pawpal_system import Task, Pet, TaskFrequency, Owner, Scheduler, ScheduledTask


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


class TestSortingCorrectness(unittest.TestCase):
    """Test that tasks are sorted in chronological order"""

    def setUp(self):
        """Create owner, pet, and scheduler with tasks at different times"""
        self.owner = Owner(
            id="owner_001",
            name="John",
            email="john@example.com"
        )
        self.pet = Pet(
            id="pet_001",
            name="Buddy",
            species="Dog",
            breed="Labrador",
            age=2
        )
        self.owner.add_pet(self.pet)
        self.scheduler = Scheduler(owner=self.owner)

    def test_sort_by_time_chronological_order(self):
        """Verify tasks are returned in chronological order when sorted by time"""
        task1 = Task(
            id="task_1",
            description="Morning walk",
            category="walk",
            duration_minutes=30,
            frequency=TaskFrequency.DAILY,
            priority="high",
            time="06:00"
        )
        task2 = Task(
            id="task_2",
            description="Evening walk",
            category="walk",
            duration_minutes=30,
            frequency=TaskFrequency.DAILY,
            priority="high",
            time="18:00"
        )
        task3 = Task(
            id="task_3",
            description="Midday feed",
            category="feed",
            duration_minutes=10,
            frequency=TaskFrequency.DAILY,
            priority="high",
            time="12:00"
        )

        self.pet.add_task(task2)
        self.pet.add_task(task3)
        self.pet.add_task(task1)

        sorted_tasks = self.scheduler.sort_by_time()
        times = [task[1].time for task in sorted_tasks]

        self.assertEqual(times, ["06:00", "12:00", "18:00"])


class TestRecurrenceLogic(unittest.TestCase):
    """Test that marking daily tasks complete creates a new task for the following day"""

    def setUp(self):
        """Create owner, pet, and scheduler"""
        self.owner = Owner(
            id="owner_002",
            name="Jane",
            email="jane@example.com"
        )
        self.pet = Pet(
            id="pet_002",
            name="Fluffy",
            species="Cat",
            breed="Siamese",
            age=3
        )
        self.owner.add_pet(self.pet)
        self.scheduler = Scheduler(owner=self.owner)

    def test_daily_task_creates_next_occurrence(self):
        """Verify marking a daily task complete creates a new task for the following day"""
        today = datetime.now()
        task = Task(
            id="task_daily_001",
            description="Feed cat",
            category="feed",
            duration_minutes=10,
            frequency=TaskFrequency.DAILY,
            priority="high",
            due_date=today
        )
        self.pet.add_task(task)

        initial_task_count = len(self.pet.tasks)
        self.scheduler.complete_task(self.pet.id, task.id)

        self.assertEqual(len(self.pet.tasks), initial_task_count + 1)

        original = self.pet.get_task("task_daily_001")
        next_task = self.pet.get_task("task_daily_001_next")

        self.assertTrue(original.is_completed)
        self.assertIsNotNone(next_task)
        self.assertFalse(next_task.is_completed)
        self.assertEqual(next_task.due_date, today + timedelta(days=1))


class TestConflictDetection(unittest.TestCase):
    """Test that the Scheduler flags duplicate/overlapping times"""

    def setUp(self):
        """Create owner, pet, and scheduler"""
        self.owner = Owner(
            id="owner_003",
            name="Bob",
            email="bob@example.com"
        )
        self.pet = Pet(
            id="pet_003",
            name="Max",
            species="Dog",
            breed="Golden Retriever",
            age=4
        )
        self.owner.add_pet(self.pet)
        self.scheduler = Scheduler(owner=self.owner)

    def test_detect_overlapping_tasks(self):
        """Verify that overlapping scheduled tasks are detected"""
        base_time = datetime(2026, 7, 7, 10, 0)

        task1 = Task(
            id="task_overlap_1",
            description="Walk",
            category="walk",
            duration_minutes=30,
            frequency=TaskFrequency.CUSTOM,
            priority="high"
        )
        task2 = Task(
            id="task_overlap_2",
            description="Bath",
            category="grooming",
            duration_minutes=30,
            frequency=TaskFrequency.CUSTOM,
            priority="high"
        )

        scheduled1 = ScheduledTask(
            task=task1,
            pet=self.pet,
            scheduled_time=base_time,
            duration_minutes=30
        )
        scheduled2 = ScheduledTask(
            task=task2,
            pet=self.pet,
            scheduled_time=base_time + timedelta(minutes=15),
            duration_minutes=30
        )

        conflict_report = self.scheduler.check_schedule_conflicts([scheduled1, scheduled2])

        self.assertIn("CONFLICT", conflict_report)

    def test_no_conflict_for_non_overlapping_tasks(self):
        """Verify that non-overlapping tasks don't trigger conflict warnings"""
        base_time = datetime(2026, 7, 7, 10, 0)

        task1 = Task(
            id="task_no_conflict_1",
            description="Walk",
            category="walk",
            duration_minutes=30,
            frequency=TaskFrequency.CUSTOM,
            priority="high"
        )
        task2 = Task(
            id="task_no_conflict_2",
            description="Feed",
            category="feed",
            duration_minutes=10,
            frequency=TaskFrequency.CUSTOM,
            priority="high"
        )

        scheduled1 = ScheduledTask(
            task=task1,
            pet=self.pet,
            scheduled_time=base_time,
            duration_minutes=30
        )
        scheduled2 = ScheduledTask(
            task=task2,
            pet=self.pet,
            scheduled_time=base_time + timedelta(minutes=30),
            duration_minutes=10
        )

        conflict_report = self.scheduler.check_schedule_conflicts([scheduled1, scheduled2])

        self.assertIn("No scheduling conflicts", conflict_report)


if __name__ == "__main__":
    unittest.main()
