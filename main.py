from pawpal_system import Task, Pet, Owner, Scheduler, TaskFrequency
from datetime import datetime


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

    # Create Tasks for Max (dog)
    task_walk_1 = Task(
        id="task_001",
        description="Morning walk",
        category="walk",
        duration_minutes=30,
        frequency=TaskFrequency.DAILY,
        priority="high"
    )

    task_feed_1 = Task(
        id="task_002",
        description="Breakfast",
        category="feed",
        duration_minutes=10,
        frequency=TaskFrequency.DAILY,
        priority="high"
    )

    task_play_1 = Task(
        id="task_003",
        description="Evening playtime",
        category="enrichment",
        duration_minutes=20,
        frequency=TaskFrequency.DAILY,
        priority="medium"
    )

    dog.add_task(task_walk_1)
    dog.add_task(task_feed_1)
    dog.add_task(task_play_1)

    # Create Tasks for Luna (cat)
    task_feed_2 = Task(
        id="task_004",
        description="Breakfast",
        category="feed",
        duration_minutes=5,
        frequency=TaskFrequency.DAILY,
        priority="high"
    )

    task_meds = Task(
        id="task_005",
        description="Give allergy medication",
        category="meds",
        duration_minutes=10,
        frequency=TaskFrequency.DAILY,
        priority="high"
    )

    task_groom = Task(
        id="task_006",
        description="Brush fur",
        category="grooming",
        duration_minutes=15,
        frequency=TaskFrequency.WEEKLY,
        priority="low"
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


if __name__ == "__main__":
    main()
