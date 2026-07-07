from pawpal_system import Task, Pet, Owner, Scheduler, ScheduledTask, TaskFrequency
from datetime import datetime, timedelta

def main():
    # Create an Owner
    owner = Owner(
        id="owner_001",
        name="Alice Johnson",
        email="alice@example.com"
    )
    print(f"Created owner: {owner.name}\n")

    # Create two Pets
    dog = Pet(
        id="pet_001",
        name="Max",
        species="Dog",
        breed="Golden Retriever",
        age=3
    )

    cat = Pet(
        id="pet_002",
        name="Luna",
        species="Cat",
        breed="Siamese",
        age=2
    )

    owner.add_pet(dog)
    owner.add_pet(cat)
    print(f"Added pets: {dog.name} and {cat.name}\n")

    # Create Tasks for Max (dog) - added out of order
    task_walk_1 = Task(
        id="task_001",
        description="Morning walk",
        category="walk",
        duration_minutes=30,
        frequency=TaskFrequency.DAILY,
        priority="high",
        time="14:30"
    )

    task_feed_1 = Task(
        id="task_002",
        description="Breakfast",
        category="feed",
        duration_minutes=10,
        frequency=TaskFrequency.DAILY,
        priority="high",
        time="08:00"
    )

    task_play_1 = Task(
        id="task_003",
        description="Evening playtime",
        category="enrichment",
        duration_minutes=20,
        frequency=TaskFrequency.DAILY,
        priority="medium",
        time="18:00"
    )

    dog.add_task(task_walk_1)
    dog.add_task(task_feed_1)
    dog.add_task(task_play_1)

    # Create Tasks for Luna (cat) - added out of order
    task_feed_2 = Task(
        id="task_004",
        description="Breakfast",
        category="feed",
        duration_minutes=5,
        frequency=TaskFrequency.DAILY,
        priority="high",
        time="07:30"
    )

    task_meds = Task(
        id="task_005",
        description="Give allergy medication",
        category="meds",
        duration_minutes=10,
        frequency=TaskFrequency.DAILY,
        priority="high",
        time="12:00"
    )

    task_groom = Task(
        id="task_006",
        description="Brush fur",
        category="grooming",
        duration_minutes=15,
        frequency=TaskFrequency.WEEKLY,
        priority="low",
        time="19:00"
    )

    cat.add_task(task_feed_2)
    cat.add_task(task_meds)
    cat.add_task(task_groom)

    print("Added tasks to pets:")
    for pet in owner.pets:
        print(f"\n{pet}:")
        for task in pet.tasks:
            print(f"  {task}")

    # Create Scheduler
    scheduler = Scheduler(owner)

    # Generate Today's Schedule
    print("\n" + "=" * 60)
    print("TODAY'S SCHEDULE")
    print("=" * 60)

    today = datetime.now()
    daily_plan = scheduler.create_daily_plan(today)

    if daily_plan:
        for scheduled in daily_plan:
            end_time = scheduled.end_time()
            print(f"{scheduled.scheduled_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')} | {scheduled.pet.name}: {scheduled.task.description} ({scheduled.task.priority})")
    else:
        print("No tasks scheduled for today.")

    print("\n" + "-" * 60)
    print(f"Total time required: {scheduler.estimate_daily_time()} minutes")
    print(f"Owner availability: {owner.availability_start} - {owner.availability_end}")
    print("-" * 60)

    # Print summary
    print("\n" + "=" * 60)
    print("OWNER SUMMARY")
    print("=" * 60)
    print(scheduler.get_owner_summary())
    
    # Demonstrate SORTING by time
    print("\n" + "=" * 60)
    print("TASKS SORTED BY TIME (HH:MM)")
    print("=" * 60)
    sorted_tasks = scheduler.sort_by_time()
    for pet, task in sorted_tasks:
        print(f"{task.time} | {pet.name}: {task.description} ({task.priority})")

    # Demonstrate FILTERING by pet name
    print("\n" + "=" * 60)
    print("FILTERING BY PET NAME")
    print("=" * 60)

    max_tasks = scheduler.filter_tasks(pet_name="Max")
    print(f"\nAll tasks for Max ({len(max_tasks)} tasks):")
    for pet, task in max_tasks:
        status = "✓" if task.is_completed else "○"
        print(f"  {status} {task.time} | {task.description} ({task.priority})")

    luna_tasks = scheduler.filter_tasks(pet_name="Luna")
    print(f"\nAll tasks for Luna ({len(luna_tasks)} tasks):")
    for pet, task in luna_tasks:
        status = "✓" if task.is_completed else "○"
        print(f"  {status} {task.time} | {task.description} ({task.priority})")

    # Demonstrate FILTERING by completion status
    print("\n" + "=" * 60)
    print("FILTERING BY COMPLETION STATUS")
    print("=" * 60)

    incomplete_tasks = scheduler.filter_tasks(completed=False)
    print(f"\nIncomplete tasks ({len(incomplete_tasks)} tasks):")
    for pet, task in incomplete_tasks:
        print(f"  ○ {task.time} | {pet.name}: {task.description} ({task.priority})")

    # Mark some tasks as completed for demonstration
    dog.get_task("task_001").mark_completed()
    cat.get_task("task_004").mark_completed()

    completed_tasks = scheduler.filter_tasks(completed=True)
    print(f"\nCompleted tasks ({len(completed_tasks)} tasks):")
    for pet, task in completed_tasks:
        print(f"  ✓ {task.time} | {pet.name}: {task.description} ({task.priority})")

    # Demonstrate FILTERING with both parameters
    print("\n" + "=" * 60)
    print("FILTERING BY PET AND COMPLETION STATUS")
    print("=" * 60)

    max_incomplete = scheduler.filter_tasks(pet_name="Max", completed=False)
    print(f"\nIncomplete tasks for Max ({len(max_incomplete)} tasks):")
    for pet, task in max_incomplete:
        print(f"  ○ {task.time} | {task.description} ({task.priority})")

    luna_completed = scheduler.filter_tasks(pet_name="Luna", completed=True)
    print(f"\nCompleted tasks for Luna ({len(luna_completed)} tasks):")
    for pet, task in luna_completed:
        print(f"  ✓ {task.time} | {task.description} ({task.priority})")

    # Demonstrate RECURRING TASK LOGIC
    print("\n" + "=" * 60)
    print("RECURRING TASK DEMONSTRATION")
    print("=" * 60)

    print(f"\nBefore completion: Max has {len(dog.tasks)} tasks")
    print("Max's tasks:")
    for task in dog.tasks:
        status = "✓" if task.is_completed else "○"
        freq = task.frequency.name
        print(f"  {status} {task.description} ({freq}) - Due: {task.due_date.strftime('%Y-%m-%d')}")

    print("\n→ Completing 'Breakfast' task for Max (DAILY task)...")
    scheduler.complete_task("pet_001", "task_002")

    print(f"\nAfter completion: Max has {len(dog.tasks)} tasks")
    print("Max's tasks:")
    for task in dog.tasks:
        status = "✓" if task.is_completed else "○"
        freq = task.frequency.name
        print(f"  {status} {task.description} ({freq}) - Due: {task.due_date.strftime('%Y-%m-%d')}")

    print("\n→ Completing 'Brush fur' task for Luna (WEEKLY task)...")
    scheduler.complete_task("pet_002", "task_006")

    print(f"\nAfter completion: Luna has {len(cat.tasks)} tasks")
    print("Luna's tasks:")
    for task in cat.tasks:
        status = "✓" if task.is_completed else "○"
        freq = task.frequency.name
        due_str = task.due_date.strftime('%Y-%m-%d')
        print(f"  {status} {task.description} ({freq}) - Due: {due_str}")

    print("\n" + "-" * 60)
    print("KEY INSIGHTS:")
    print("  • Daily tasks create new instances for tomorrow (today + 1 day)")
    print("  • Weekly tasks create new instances for next week (today + 7 days)")
    print("  • Uses Python's timedelta() to calculate next occurrence dates")
    print("  • Original completed task remains in history")
    print("-" * 60)

    # Demonstrate LIGHTWEIGHT CONFLICT DETECTION
    print("\n" + "=" * 60)
    print("LIGHTWEIGHT CONFLICT DETECTION")
    print("=" * 60)

    print("\n--- Scenario 1: No Conflicts (Sequential Schedule) ---")
    today = datetime.now()
    conflict_free_schedule = [
        ScheduledTask(task_feed_1, dog, datetime.combine(today.date(), datetime.strptime("08:00", "%H:%M").time()), 10),
        ScheduledTask(task_walk_1, dog, datetime.combine(today.date(), datetime.strptime("08:15", "%H:%M").time()), 30),
        ScheduledTask(task_play_1, dog, datetime.combine(today.date(), datetime.strptime("08:50", "%H:%M").time()), 20),
    ]

    print("Tasks:")
    for st in conflict_free_schedule:
        print(f"  {st.scheduled_time.strftime('%H:%M')} - {st.end_time().strftime('%H:%M')} | {st.pet.name}: {st.task.description}")

    result = scheduler.check_schedule_conflicts(conflict_free_schedule)
    print(f"\nCheck result:\n  {result}")

    print("\n--- Scenario 2: Overlapping Tasks (Same Pet) ---")
    conflicting_schedule = [
        ScheduledTask(task_feed_1, dog, datetime.combine(today.date(), datetime.strptime("08:00", "%H:%M").time()), 20),
        ScheduledTask(task_walk_1, dog, datetime.combine(today.date(), datetime.strptime("08:10", "%H:%M").time()), 30),
        ScheduledTask(task_play_1, dog, datetime.combine(today.date(), datetime.strptime("09:00", "%H:%M").time()), 20),
    ]

    print("Tasks:")
    for st in conflicting_schedule:
        print(f"  {st.scheduled_time.strftime('%H:%M')} - {st.end_time().strftime('%H:%M')} | {st.pet.name}: {st.task.description}")

    result = scheduler.check_schedule_conflicts(conflicting_schedule)
    print(f"\nCheck result:\n  {result}")

    print("\n--- Scenario 3: Conflicts Across Multiple Pets ---")
    multi_pet_conflicts = [
        ScheduledTask(task_feed_1, dog, datetime.combine(today.date(), datetime.strptime("10:00", "%H:%M").time()), 15),
        ScheduledTask(task_feed_2, cat, datetime.combine(today.date(), datetime.strptime("10:05", "%H:%M").time()), 10),
        ScheduledTask(task_groom, cat, datetime.combine(today.date(), datetime.strptime("10:10", "%H:%M").time()), 20),
    ]

    print("Tasks:")
    for st in multi_pet_conflicts:
        print(f"  {st.scheduled_time.strftime('%H:%M')} - {st.end_time().strftime('%H:%M')} | {st.pet.name}: {st.task.description}")

    result = scheduler.check_schedule_conflicts(multi_pet_conflicts)
    print(f"\nCheck result:\n  {result}")

    print("\n--- Scenario 4: TWO TASKS AT EXACT SAME TIME ---")
    same_time_conflict = [
        ScheduledTask(task_feed_1, dog, datetime.combine(today.date(), datetime.strptime("12:00", "%H:%M").time()), 15),
        ScheduledTask(task_feed_2, cat, datetime.combine(today.date(), datetime.strptime("12:00", "%H:%M").time()), 10),
        ScheduledTask(task_meds, cat, datetime.combine(today.date(), datetime.strptime("12:15", "%H:%M").time()), 10),
    ]

    print("Tasks:")
    for st in same_time_conflict:
        print(f"  {st.scheduled_time.strftime('%H:%M')} - {st.end_time().strftime('%H:%M')} | {st.pet.name}: {st.task.description}")

    result = scheduler.check_schedule_conflicts(same_time_conflict)
    print(f"\nCheck result:\n  {result}")

    print("\n" + "-" * 60)
    print("LIGHTWEIGHT APPROACH:")
    print("  • Returns warning messages instead of crashing")
    print("  • Single method: check_schedule_conflicts()")
    print("  • Identifies both same-pet and cross-pet conflicts")
    print("  • Non-blocking—program continues normally")
    print("-" * 60)


if __name__ == "__main__":
    main()
