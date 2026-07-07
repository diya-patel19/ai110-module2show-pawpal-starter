from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, time, timedelta
from enum import Enum


class TaskFrequency(Enum):
    """Frequency options for tasks"""
    DAILY = 1
    TWICE_DAILY = 2
    WEEKLY = 7
    CUSTOM = 0


@dataclass
class Task:
    """Represents a single activity with description, time, frequency, and completion status"""
    id: str
    description: str
    category: str  # walk, feed, meds, enrichment, grooming
    duration_minutes: int
    frequency: TaskFrequency
    priority: str  # high, medium, low
    time: str = "00:00"  # HH:MM format
    is_completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    due_date: datetime = field(default_factory=datetime.now)

    def mark_completed(self):
        """Mark task as completed"""
        self.is_completed = True

    def mark_incomplete(self):
        """Mark task as incomplete"""
        self.is_completed = False

    def create_next_occurrence(self) -> Optional['Task']:
        """Create the next occurrence of a recurring task.

        Uses timedelta to calculate: DAILY adds 1 day, WEEKLY adds 7 days.
        Returns None for CUSTOM (non-recurring) tasks.

        Returns a new Task with same attributes but is_completed=False and updated due_date.
        """
        if self.frequency == TaskFrequency.CUSTOM:
            return None

        next_due_date = self.due_date + timedelta(days=self.frequency.value)
        next_task = Task(
            id=f"{self.id}_next",
            description=self.description,
            category=self.category,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            priority=self.priority,
            time=self.time,
            is_completed=False,
            created_at=datetime.now(),
            due_date=next_due_date
        )
        return next_task

    def __str__(self) -> str:
        """Return a formatted string representation of the task."""
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.description} ({self.duration_minutes}min) - {self.priority}"


@dataclass
class Pet:
    """Stores pet details and maintains a list of tasks"""
    id: str
    name: str
    species: str  # dog, cat, bird, etc.
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's care plan"""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by id. Returns True if successful"""
        self.tasks = [t for t in self.tasks if t.id != task_id]
        return True

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a specific task by id"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_pending_tasks(self) -> List[Task]:
        """Get all incomplete tasks for this pet"""
        return [t for t in self.tasks if not t.is_completed]

    def __str__(self) -> str:
        """Return a formatted string representation of the pet."""
        pending = len(self.get_pending_tasks())
        return f"{self.name} ({self.species}/{self.breed}, age {self.age}) - {pending} pending tasks"


@dataclass
class Owner:
    """Manages multiple pets and provides unified access to all their tasks"""
    id: str
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)
    availability_start: time = field(default_factory=lambda: time(8, 0))
    availability_end: time = field(default_factory=lambda: time(22, 0))

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to owner's collection"""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> bool:
        """Remove a pet by id"""
        initial_count = len(self.pets)
        self.pets = [p for p in self.pets if p.id != pet_id]
        return len(self.pets) < initial_count

    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """Retrieve a specific pet by id"""
        for pet in self.pets:
            if pet.id == pet_id:
                return pet
        return None

    def get_all_tasks(self) -> List[tuple[Pet, Task]]:
        """Get all tasks across all pets as (pet, task) tuples"""
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))
        return all_tasks

    def get_pending_tasks(self) -> List[tuple[Pet, Task]]:
        """Get all incomplete tasks across all pets"""
        return [(pet, task) for pet, task in self.get_all_tasks() if not task.is_completed]

    def get_tasks_for_pet(self, pet_id: str) -> List[Task]:
        """Get all tasks for a specific pet"""
        pet = self.get_pet(pet_id)
        return pet.tasks if pet else []

    def __str__(self) -> str:
        """Return a formatted string representation of the owner."""
        total_tasks = len(self.get_all_tasks())
        pending = len(self.get_pending_tasks())
        return f"{self.name} ({len(self.pets)} pets, {pending}/{total_tasks} tasks pending)"


@dataclass
class ScheduledTask:
    """A task assigned to a specific time slot"""
    task: Task
    pet: Pet
    scheduled_time: datetime
    duration_minutes: int

    def end_time(self) -> datetime:
        """Calculate when this task ends"""
        return self.scheduled_time + timedelta(minutes=self.duration_minutes)

    def overlaps_with(self, other: 'ScheduledTask') -> bool:
        """Check if this task's time range overlaps with another's.

        Uses interval overlap logic: start1 < end2 AND start2 < end1.
        Detects partial overlaps, not just exact time matches.
        """

    def __str__(self) -> str:
        """Return a formatted string representation of the scheduled task."""
        return f"{self.pet.name}: {self.task.description} at {self.scheduled_time.strftime('%H:%M')}"


@dataclass
class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets"""
    owner: Owner

    def get_daily_tasks(self, date: datetime) -> List[tuple[Pet, Task]]:
        """Get all pending tasks for a specific date"""
        # Currently returns all pending tasks; could be filtered by date in future
        return self.owner.get_pending_tasks()

    def get_tasks_by_priority(self) -> List[tuple[Pet, Task]]:
        """Sort all pending tasks by priority (high > medium > low)"""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        tasks = self.owner.get_pending_tasks()
        return sorted(tasks, key=lambda x: priority_order.get(x[1].priority, 3))

    def get_tasks_by_category(self, category: str) -> List[tuple[Pet, Task]]:
        """Get all pending tasks of a specific category"""
        return [(pet, task) for pet, task in self.owner.get_pending_tasks() if task.category == category]

    def sort_by_time(self) -> List[tuple[Pet, Task]]:
        """Sort all pending tasks by time in HH:MM format (earliest to latest).

        Uses sorted() with lambda key on the time attribute.
        HH:MM strings sort lexicographically in chronological order.
        """

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[tuple[Pet, Task]]:
        """Filter tasks by completion status and/or pet name.

        Args:
            completed: True for completed only, False for incomplete, None for all
            pet_name: Filter by pet name (case-insensitive), None for all pets

        Both filters use AND logic if provided together.
        """
        tasks = self.owner.get_all_tasks()

        if completed is not None:
            tasks = [t for t in tasks if t[1].is_completed == completed]

        if pet_name is not None:
            tasks = [t for t in tasks if t[0].name.lower() == pet_name.lower()]

        return tasks

    def estimate_daily_time(self) -> int:
        """Calculate total time needed for all pending tasks (in minutes)"""
        total_minutes = 0
        for _, task in self.owner.get_pending_tasks():
            total_minutes += task.duration_minutes
        return total_minutes

    def create_daily_plan(self, date: datetime) -> List[ScheduledTask]:
        """Generate daily schedule by packing tasks in priority order.

        Sorts tasks by priority (high→low), fits each sequentially into available time.
        Drops tasks that don't fit before availability_end.

        Constraints: owner availability, task priority, task duration.
        Note: Uses sequential packing, not global optimization.
        """

    def complete_task(self, pet_id: str, task_id: str) -> bool:
        """Mark task as completed and auto-create next occurrence if recurring.

        For DAILY/WEEKLY tasks, calls create_next_occurrence() and adds to pet's tasks.
        Returns False if pet or task not found.
        """
        pet = self.owner.get_pet(pet_id)
        if not pet:
            return False

        task = pet.get_task(task_id)
        if not task:
            return False

        task.mark_completed()

        if task.frequency != TaskFrequency.CUSTOM:
            next_task = task.create_next_occurrence()
            if next_task:
                pet.add_task(next_task)

        return True

    def check_schedule_conflicts(self, scheduled_tasks: List[ScheduledTask]) -> str:
        """Detect scheduling conflicts and return warning messages (non-blocking).

        Scans all task pairs for overlaps. Returns formatted warnings instead of exceptions.
        "✓ No scheduling conflicts detected" if no overlaps found.
        """
        if not scheduled_tasks:
            return "✓ No tasks scheduled"

        warnings = []
        checked_pairs = set()

        for i in range(len(scheduled_tasks)):
            for j in range(i + 1, len(scheduled_tasks)):
                task1, task2 = scheduled_tasks[i], scheduled_tasks[j]

                pair_key = (min(i, j), max(i, j))
                if pair_key in checked_pairs:
                    continue
                checked_pairs.add(pair_key)

                if task1.overlaps_with(task2):
                    pet_info = ""
                    if task1.pet.id == task2.pet.id:
                        pet_info = f" (same pet: {task1.pet.name})"

                    warning = (
                        f"⚠️  CONFLICT{pet_info}: "
                        f"'{task1.task.description}' ({task1.scheduled_time.strftime('%H:%M')}) "
                        f"overlaps with '{task2.task.description}' ({task2.scheduled_time.strftime('%H:%M')})"
                    )
                    warnings.append(warning)

        if not warnings:
            return "✓ No scheduling conflicts detected"

        return "\n".join(warnings)

    def get_owner_summary(self) -> str:
        """Get a summary of all tasks across all pets"""
        summary = str(self.owner) + "\n"
        for pet in self.owner.pets:
            summary += f"  • {pet}\n"
        return summary
