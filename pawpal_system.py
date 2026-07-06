from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Task:
    """Represents a pet care task"""
    id: str
    name: str
    category: str
    frequency_per_week: int
    duration_minutes: int
    priority: str


@dataclass
class Pet:
    """Represents a pet and its care tasks"""
    id: str
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)


@dataclass
class Constraint:
    """Scheduling constraint (time windows, availability)"""
    type: str
    start_time: datetime
    end_time: datetime
    available_days: List[str] = field(default_factory=list)

    def is_satisfied(self, time_slot: datetime) -> bool:
        pass


@dataclass
class DailyPlan:
    """Generated daily schedule with reasoning"""
    date: datetime
    tasks: List[Task] = field(default_factory=list)
    rationale: str = ""

    def generate(self, pet: Pet) -> None:
        """Generate daily plan for the pet"""
        pass
