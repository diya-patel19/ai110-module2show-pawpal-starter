# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

Created owner: Alice Johnson

Added pets: Max and Luna

Added tasks to pets:

Max (Dog/Golden Retriever, age 3) - 3 pending tasks:
  ○ Morning walk (30min) - high
  ○ Breakfast (10min) - high
  ○ Evening playtime (20min) - medium

Luna (Cat/Siamese, age 2) - 3 pending tasks:
  ○ Breakfast (5min) - high
  ○ Give allergy medication (10min) - high
  ○ Brush fur (15min) - low

============================================================
TODAY'S SCHEDULE
============================================================
08:00 - 08:30 | Max: Morning walk (high)
08:30 - 08:40 | Max: Breakfast (high)
08:40 - 08:45 | Luna: Breakfast (high)
08:45 - 08:55 | Luna: Give allergy medication (high)
08:55 - 09:15 | Max: Evening playtime (medium)
09:15 - 09:30 | Luna: Brush fur (low)

------------------------------------------------------------
Total time required: 90 minutes
Owner availability: 08:00:00 - 22:00:00
------------------------------------------------------------

============================================================
OWNER SUMMARY
============================================================
Alice Johnson (2 pets, 6/6 tasks pending)
  • Max (Dog/Golden Retriever, age 3) - 3 pending tasks
  • Luna (Cat/Siamese, age 2) - 3 pending tasks

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```
Command to run tests: python3 -m pytest

Terminal output if all tests successful: 
test_pawpal.py ...........                                                                                                                                                                     [100%]

========================================================================================= 11 passed in 0.02s =========================================================================================

The pytests written tests various features across the app. This includes adding tasks, completing tasks, sorting tasks, recurring tasks, and confliction of tasks in the schedule. My confidence level on this app is 4 stars out of 5. It has passed all the tests entirely without bugging out, but it is still possible that there are some bugs and imperfections.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature           | Method(s)                                  | Notes                                 |
|-------------------|--------------------------------------------|---------------------------------------|
| Task sorting      | create_daily_plan()                        | sorts tasks by priority + availablity |
| Filtering         | complete_task()                            | marks complete + recurrence           |
| Conflict handling | estimate_daily_time()                      | sums pending task durations           |
| Recurring tasks   | get_daily_tasks(), get_tasks_by_category() | get tasks by date/category            |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
