# PawPal+ Project Reflection

## 1. System Design

Three core actions that the user must be able to preform is add one or multiple pets with specific informaiton on each, block out times in their schedule when they are unable to engage in activities such as taking their pet for a walk, and see what needs to be done every day in terms of things like walks, food, medications, etc. for each of their pets. 

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The classes that I included included were Pet, Task, Constraint, and DailyPlan. The Pet class represents the owners pets with attributes describing each pet. It also manages tasks regarding the pet. The Task class defines specific care activities, and properties include frequency, duration, and priotity. The Constraint class contains all the scheduling rtules and similation. And the DailyPlan class takes all the information and creates an optimized daily plan for the user to follow. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, the design slightly changed during implementaion. One change I made was adding logic to DailyPlan to create a schedule. Originally, it just stored tasks, but using the AI agent, I was able to add logic that shows when the tasks and scheduled during the day. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
