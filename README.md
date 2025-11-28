# Smart Task Analyzer

**A Django-based task intelligence system that scores and prioritizes workload using a weighted multi-factor algorithm.**

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Setup & Installation](#-setup--installation)
3. [The Scoring Algorithm (Core Logic)](#-the-scoring-algorithm-core-logic)
4. [Architecture & Design Decisions](#-architecture--design-decisions)
5. [Key Features](#-key-features)
6. [Testing](#-testing)
7. [Time Breakdown](#-time-breakdown)
8. [Future Improvements](#-future-improvements)

---

## 📖 Project Overview
The **Smart Task Analyzer** is designed to solve decision paralysis. Instead of a simple "To-Do" list that sorts tasks merely by date, this application uses a sophisticated backend algorithm to calculate a **Priority Score** for every task.

The system evaluates four distinct dimensions of every task: **Urgency** (Time), **Importance** (Value), **Effort** (Cost), and **Dependencies** (Blockers), providing the user with a scientifically prioritized list of what to work on next.

**Tech Stack:**
* **Backend:** Python 3.8+, Django 4.0+, Django REST Framework
* **Frontend:** HTML5, CSS3 (Modern Variables), Vanilla JavaScript (ES6+)
* **Database:** SQLite (Default)

---

## Setup & Installation

### 1. Prerequisites
* Python 3.8 or higher installed.
* `pip` (Python package manager).

### 2. Backend Setup
```bash
# Clone the repository
git clone <your-repo-link-here>
cd task-analyzer

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Navigate to backend and setup database
cd backend
python manage.py migrate

# Run the server
python manage.py runserver
```

### 3. Frontend Setup
The frontend is designed to be lightweight and decoupled.

* Navigate to the frontend/ folder in your file explorer.

* Open index.html in any modern web browser (Chrome, Firefox, Edge).

* The frontend will automatically connect to your local Django server.


---

## The Scoring Algorithm (Core Logic)
The heart of this application is the "Smart Balance" algorithm, located in backend/tasks/scoring.py. It assigns a numerical score ($S$) to each task, where a higher score equals higher priority.

### The Formula: $S = U + (I \times 5) + D + E$

1. Urgency ($U$): The Time Factor
Urgency is not linear. A task due in 30 days is effectively "zero urgency," but a task due yesterday is critical. The algorithm handles this via dynamic scaling:
* Overdue Logic: If the due date is in the past ($d < 0$), the score skyrockets using the formula $100 + (|d| \times 2)$. A task 10 days late receives 120 points immediately, ensuring it dominates the top of the list regardless of importance.
* Imminent Deadlines: Tasks due today or tomorrow receive a flat high score (75 points) to ensure they are cleared before becoming overdue.
* Decay Curve: For future tasks, the score decays linearly. A task due in 7 days gets significantly fewer points than one due in 3 days.

2. Importance ($I$): The Value Factor
Users rate tasks on a 1-10 scale. However, on a raw scale, a "10" (Critical Importance) is numerically tiny compared to a "100" (Urgency).
* The Multiplier: To correct this, we multiply Importance by 5.
* The Result: A critical "Life Goal" task (Importance 10) now receives 50 points. This puts it on par with a task due in 2-3 days, ensuring that high-value strategic work isn't buried by low-value busy work.

3. Dependencies ($D$): The Bottleneck Theory
In project management, blocking tasks (bottlenecks) are more valuable than leaf tasks.
* Scoring: We add +10 points for every other task that lists the current task as a dependency.
* Why? Clearing a task that blocks 3 others unlocks productivity for the rest of the queue. This is a "Force Multiplier."

4. Effort ($E$): Momentum Psychology
Finally, we consider the psychological aspect of productivity.
* Quick Wins: If a task takes $\le$ 2 hours, it gets a +10 point bonus.
* Why? David Allen’s Getting Things Done methodology suggests that clearing small tasks quickly builds momentum. This small bonus pushes "easy" tasks up the list slightly, breaking inertia without overshadowing critical deadlines.


## Design Decisions & Trade-offs

### 1. Decoupled Architecture (REST API)
* Decision: I chose to separate the Frontend (HTML/JS) from the Backend (Django Views), connecting them via REST API.

* Trade-off: This required handling CORS (Cross-Origin Resource Sharing) and writing fetch logic in JavaScript, which is more complex than standard Django Templates.

* Benefit: This enforces a clean separation of concerns. The backend is now a pure microservice. In the future, this same API could power a React Native mobile app without changing a single line of Python code.

### 2. Stateless Analysis Endpoint
* Decision: The /api/tasks/analyze/ (POST) endpoint accepts a JSON list and returns sorted results without saving them to the database.

* Trade-off: Requires the frontend to manage "staged" state before the user commits to saving.

* Benefit: This allows for a "Playground Mode." Users can paste hypothetical task lists (JSON) to see how the AI prioritizes them without polluting their persistent database with junk data.

### 3. Client-Side Strategy Toggling
* Decision: While the "Smart Balance" score is calculated on the server, the sorting toggle (switching between "Urgent", "Important", "Smart") is handled in the browser's JavaScript.

* Trade-off: The browser must hold the data array in memory.

* Benefit: Instant UX. The user gets zero-latency feedback when switching views, making the interface feel snappy and responsive compared to reloading the page from the server for every sort change.


## Time Breakdown
| Component                   | Time Spent   | Notes                                      |
|----------------------------|--------------|---------------------------------------------|
| Project Structure & Env    | 30 mins      | Setup venv, Django, folders                 |
| Algorithm Design           | 45 mins      | Designing the formula & edge cases          |
| Backend Logic (API)        | 1.5 hours    | Models, Serializers, Views                  |
| Frontend Implementation    | 1.5 hours    | CSS Grid, JS Fetch, Dynamic UI              |
| Testing & Documentation    | 45 mins      | test_api.py and README                      |
| **Total**                  | **~4.5 Hours** |                                             |


## Bonus Challenges
* Unit Tests: Implemented a standalone python script (test_api.py) to verify the scoring logic against edge cases (Overdue dates, Missing dates) before connecting the frontend.

* Sorting Strategies: Implemented a UI toggle to switch between "Smart Balance", "Deadline Driven", and "Fastest Wins".


## Future Improvements
With more time, I would implement:

1. Eisenhower Matrix View: A 2D grid visualization plotting Urgency (X-axis) vs. Importance (Y-axis).

2. Circular Dependency Detection: A recursive check in the Python backend to prevent tasks from blocking each other (A -> B -> A).

3. Authentication: Simple JWT authentication to allow multiple users to maintain private task lists.