# PawPal Class Diagram

```mermaid
classDiagram
    class User {
        -userId: string
        -name: string
        -email: string
        -preferences: Map~string, any~
        +addPet(pet: Pet): void
        +removePet(petId: string): void
        +getPets(): Pet[]
        +getScheduleConstraints(): ScheduleConstraint[]
        +addScheduleConstraint(constraint: ScheduleConstraint): void
    }

    class Pet {
        -petId: string
        -name: string
        -species: string
        -breed: string
        -age: number
        -weight: number
        -healthInfo: string
        +getTasks(): CareTask[]
        +getSchedule(): TaskSchedule[]
        +updateHealthInfo(info: string): void
    }

    class CareTask {
        -taskId: string
        -type: TaskType
        -name: string
        -description: string
        -durationMinutes: number
        -frequency: Frequency
        -priority: Priority
        -notes: string
        +isOverdue(lastCompleted: Date): boolean
        +getNextDueDate(): Date
    }

    class Frequency {
        -count: number
        -unit: 'daily'~'weekly'~'monthly'
        +getNextOccurrence(lastDate: Date): Date
    }

    class TaskType {
        <<enumeration>>
        WALK
        FEEDING
        MEDICATION
        GROOMING
        PLAY_ENRICHMENT
        TRAINING
        VET_CHECKUP
    }

    class Priority {
        <<enumeration>>
        CRITICAL
        HIGH
        MEDIUM
        LOW
    }

    class ScheduleConstraint {
        -constraintId: string
        -startTime: Time
        -endTime: Time
        -daysOfWeek: Day[]
        -reason: string
        -isRecurring: boolean
        +isAvailable(dateTime: DateTime): boolean
    }

    class DailyPlan {
        -planId: string
        -date: Date
        -plannedTasks: PlannedTask[]
        -totalDurationMinutes: number
        +generatePlan(pets: Pet[], constraints: ScheduleConstraint[]): void
        +getExplanation(): string
        +markTaskComplete(taskId: string): void
        +getPrioritizedTasks(): PlannedTask[]
    }

    class PlannedTask {
        -plannedTaskId: string
        -careTask: CareTask
        -pet: Pet
        -suggestedTime: DateTime
        -rationale: string
        -isCompleted: boolean
        +reschedule(newTime: DateTime): void
        +complete(actualTime: DateTime): void
    }

    class TaskSchedule {
        -scheduleId: string
        -careTask: CareTask
        -completedDates: Date[]
        -nextDueDate: Date
        +logCompletion(date: Date): void
        +getCompletionHistory(): CompletionRecord[]
    }

    class CompletionRecord {
        -recordId: string
        -taskId: string
        -completedDate: DateTime
        -notes: string
        -duration: number
    }

    class PlanOptimizer {
        +generateDailyPlan(pets: Pet[], constraints: ScheduleConstraint[], preferences: Map): DailyPlan
        -calculateTaskPriorities(tasks: CareTask[]): CareTask[]
        -findAvailableSlots(constraints: ScheduleConstraint[]): TimeSlot[]
        -assignTasksToSlots(tasks: CareTask[], slots: TimeSlot[]): PlannedTask[]
        -generateExplanation(plan: DailyPlan): string
    }

    class TimeSlot {
        -slotId: string
        -startTime: DateTime
        -endTime: DateTime
        -durationMinutes: number
        +canFit(task: CareTask): boolean
    }

    User "1" --> "0..*" Pet
    User "1" --> "0..*" ScheduleConstraint
    Pet "1" --> "0..*" CareTask
    Pet "1" --> "0..*" TaskSchedule
    CareTask "1" --> "1" TaskType
    CareTask "1" --> "1" Priority
    CareTask "1" --> "1" Frequency
    DailyPlan "1" --> "0..*" PlannedTask
    PlannedTask "1" --> "1" CareTask
    PlannedTask "1" --> "1" Pet
    TaskSchedule "1" --> "1" CareTask
    TaskSchedule "1" --> "0..*" CompletionRecord
    PlanOptimizer "1" --> "0..*" DailyPlan
    PlanOptimizer "1" ..> "0..*" TimeSlot
```

## Key Design Concepts

**User Management**
- Users can manage multiple pets and schedule constraints
- Preferences allow customization of plan generation

**Pet & Care Tasks**
- Each pet has multiple care tasks with different types, frequencies, and priorities
- Tasks track duration and dependencies

**Planning & Optimization**
- PlanOptimizer generates daily plans based on pets, constraints, and preferences
- PlannedTask includes rationale for why a task is scheduled at a specific time
- Daily plans explain their logic to the user

**Tracking & History**
- TaskSchedule maintains completion history
- CompletionRecord logs when tasks were actually completed

**Constraints**
- ScheduleConstraint models owner availability (blocked times)
- Supports recurring constraints
