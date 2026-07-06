```mermaid
classDiagram
    class Pet {
        +String id
        +String name
        +String species
        +String breed
        +int age
        +List~Task~ tasks
        +addTask(Task)
        +getTasks()
    }

    class Task {
        +String id
        +String name
        +String category
        +int frequencyDaysPerWeek
        +int durationMinutes
        +String priority
        +List~Constraint~ constraints
        +getConstraints()
    }

    class Constraint {
        +String id
        +String type
        +String description
        +boolean isSatisfied(TimeSlot)
    }

    class TimeConstraint {
        +Time earliestTime
        +Time latestTime
        +List~String~ availableDays
    }

    class PriorityConstraint {
        +int priorityLevel
        +List~String~ preferredTimeOfDay
    }

    class OwnerPreference {
        +String id
        +String preferenceType
        +String value
        +int weight
    }

    class DailyPlan {
        +String date
        +List~ScheduledTask~ scheduledTasks
        +String planningRationale
        +addScheduledTask(ScheduledTask)
        +getPlanRationale()
    }

    class ScheduledTask {
        +String taskId
        +Time scheduledTime
        +int durationMinutes
        +boolean isCompleted
        +String notes
        +markAsCompleted()
    }

    class PlanGenerator {
        +generateDailyPlan(Pet, List~OwnerPreference~)
        +calculateOptimalTimeSlots(Task, List~Constraint~)
        +checkConstraintSatisfaction(Task, TimeSlot)
        -scoreSchedule(DailyPlan)
    }

    class ScheduleOptimizer {
        +optimizeSchedule(List~Task~, List~Constraint~)
        +resolveConflicts(ScheduledTask, ScheduledTask)
        -calculateFitness(Assignment)
    }

    Pet "1" *-- "*" Task : has
    Task "1" *-- "*" Constraint : has
    Constraint <|-- TimeConstraint
    Constraint <|-- PriorityConstraint
    Pet "1" -- "*" OwnerPreference : preferences
    Pet "1" -- "*" DailyPlan : generates
    DailyPlan "1" *-- "*" ScheduledTask : contains
    ScheduledTask "1" -- "1" Task : references
    PlanGenerator -- Pet : uses
    PlanGenerator -- DailyPlan : creates
    ScheduleOptimizer -- "1" Pet : optimizes
```

## Pet Care App - Class Diagram

### Core Classes:
- **Pet** — Represents a pet and its associated tasks
- **Task** — A care activity (walk, feed, meds, etc.) with frequency and duration
- **Constraint** — Abstract class for scheduling constraints (time-based, priority-based)
- **OwnerPreference** — Owner's scheduling preferences (time of day, priority weight)
- **DailyPlan** — Generated schedule with reasoning for the pet's daily activities
- **ScheduledTask** — A task assigned to a specific time slot
- **PlanGenerator** — Creates optimal daily plans considering all constraints
- **ScheduleOptimizer** — Resolves conflicts and optimizes task ordering

### Key Features:
- Tracks multiple task types (walks, feeding, meds, enrichment, grooming)
- Supports flexible constraints (time windows, availability, priorities)
- Generates daily plans with explanations of scheduling decisions
- Allows owner preferences to influence plan generation
