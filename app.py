import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler, TaskFrequency, ScheduledTask
from datetime import datetime

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = None

if "selected_pet_id" not in st.session_state:
    st.session_state.selected_pet_id = None

st.subheader("👤 Owner Setup")
owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@example.com")

# Create or update owner in session
if st.button("Create/Update Owner", key="create_owner"):
    st.session_state.owner = Owner(
        id="owner_001",
        name=owner_name,
        email=owner_email
    )
    st.session_state.selected_pet_id = None
    st.success(f"Owner '{owner_name}' created!")

st.divider()

# Pet Management Section
if st.session_state.owner:
    st.subheader("🐾 Manage Pets")

    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"])
    with col3:
        breed = st.text_input("Breed", value="Mixed")

    pet_age = st.slider("Age (years)", 1, 20, 5)

    if st.button("Add Pet"):
        new_pet = Pet(
            id=f"pet_{len(st.session_state.owner.pets) + 1:03d}",
            name=pet_name,
            species=species,
            breed=breed,
            age=pet_age
        )
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Pet '{pet_name}' added!")

    # Display current pets
    if st.session_state.owner.pets:
        st.write("**Current Pets:**")
        for pet in st.session_state.owner.pets:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"🐾 {pet.name} ({pet.species}/{pet.breed}, age {pet.age})")
            with col2:
                if st.button("Select", key=f"select_{pet.id}"):
                    st.session_state.selected_pet_id = pet.id

    st.divider()

    # Task Management Section
    if st.session_state.selected_pet_id:
        selected_pet = st.session_state.owner.get_pet(st.session_state.selected_pet_id)
        st.subheader(f"📋 Add Tasks for {selected_pet.name}")

        col1, col2, col3 = st.columns(3)
        with col1:
            task_description = st.text_input("Task description", value="Morning walk")
        with col2:
            category = st.selectbox("Category", ["walk", "feed", "meds", "enrichment", "grooming"])
        with col3:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=30)

        col1, col2 = st.columns(2)
        with col1:
            priority = st.selectbox("Priority", ["low", "medium", "high"])
        with col2:
            frequency = st.selectbox("Frequency", [f.name for f in TaskFrequency])

        if st.button("Add Task"):
            new_task = Task(
                id=f"task_{len(selected_pet.tasks) + 1:03d}",
                description=task_description,
                category=category,
                duration_minutes=int(duration),
                frequency=TaskFrequency[frequency],
                priority=priority
            )
            selected_pet.add_task(new_task)
            st.success(f"Task '{task_description}' added to {selected_pet.name}!")

        # Display pet's tasks
        if selected_pet.tasks:
            st.write(f"**Tasks for {selected_pet.name}:**")
            for task in selected_pet.tasks:
                st.write(f"  • {task}")
        else:
            st.info(f"No tasks yet for {selected_pet.name}")
    else:
        st.info("Select a pet to add tasks")

    st.divider()

    # Schedule Generation Section
    st.subheader("📅 Generate Daily Schedule")

    if st.button("Generate Schedule"):
        scheduler = Scheduler(st.session_state.owner)
        today = datetime.now()
        daily_plan = scheduler.create_daily_plan(today)

        if daily_plan:
            st.success("Schedule generated!")
            st.write(f"**Schedule for {today.strftime('%A, %B %d, %Y')}**")

            schedule_data = []
            for scheduled in daily_plan:
                end_time = scheduled.end_time()
                schedule_data.append({
                    "Time": f"{scheduled.scheduled_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}",
                    "Pet": scheduled.pet.name,
                    "Task": scheduled.task.description,
                    "Priority": scheduled.task.priority.upper(),
                    "Duration": f"{scheduled.task.duration_minutes}min"
                })

            st.table(schedule_data)
            st.metric("Total Time Required", f"{scheduler.estimate_daily_time()} minutes")
        else:
            st.info("No tasks scheduled. Add tasks to pets first.")

    # Summary Section
    st.divider()
    st.subheader("📊 Summary")
    scheduler = Scheduler(st.session_state.owner)
    st.write(scheduler.get_owner_summary())

else:
    st.info("Create an owner to get started!")
