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
    is_completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def mark_completed(self):
        """Mark task as completed"""
        self.is_completed = True

    def mark_incomplete(self):
        """Mark task as incomplete"""
        self.is_completed = False

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

    def estimate_daily_time(self) -> int:
        """Calculate total time needed for all pending tasks (in minutes)"""
        total_minutes = 0
        for _, task in self.owner.get_pending_tasks():
            total_minutes += task.duration_minutes
        return total_minutes

    def create_daily_plan(self, date: datetime) -> List[ScheduledTask]:
        """Generate a daily schedule for all pets considering time constraints and priorities"""
        pending_tasks = self.get_tasks_by_priority()
        scheduled = []
        current_time = datetime.combine(date.date(), self.owner.availability_start)
        end_time = datetime.combine(date.date(), self.owner.availability_end)

        for pet, task in pending_tasks:
            # Check if task fits in remaining time
            task_end = current_time + timedelta(minutes=task.duration_minutes)
            if task_end <= end_time:
                scheduled_task = ScheduledTask(task, pet, current_time, task.duration_minutes)
                scheduled.append(scheduled_task)
                current_time = task_end

        return scheduled

    def get_owner_summary(self) -> str:
        """Get a summary of all tasks across all pets"""
        summary = str(self.owner) + "\n"
        for pet in self.owner.pets:
            summary += f"  • {pet}\n"
        return summary
