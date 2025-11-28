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

### The Formula:$$S = U + (I \times 5) + D + E

1. Urgency ($U$) - "The Time Factor"
We calculate the days remaining ($d$) until the deadline.
* Overdue Tasks ($d < 0$): These are critical. We apply a base score of 100 plus a penalty for every day late ($100 + |d| \times 2$). A task 10 days late gets a massive 120 points.
* Imminent (0-2 days): High priority base score (75 to 50 points).
* Future (> 7 days): Low urgency score that decays as the date gets further away.
* Missing Dates: Treated as low urgency to prevent system crashes, ensuring robustness.

2. Importance ($I$) - "The Value Factor"
Users rate tasks on a 1-10 scale.
* Weighting: We multiply this value by 5.
* Rationale: A standard 1-10 scale is too weak against the massive points from "Urgency". By multiplying by 5, a "Life Goal" task (Importance 10) gets 50 points—equivalent to a task due tomorrow. This ensures important work isn't always buried by trivial urgent work.

3. Dependencies ($D$) - "The Bottleneck Factor"
* Logic: $+10$ points for every other task that is strictly waiting on this task.
* Rationale: If "Task A" blocks 3 other tasks, finishing "Task A" unlocks significant value. It serves as a force multiplier for productivity.

4. Effort ($E$) - "The Momentum Factor"
* Quick Wins: If estimated_hours $\le$ 2, we add +10 points.
* Rationale: Behavioral psychology suggests that completing small tasks early builds momentum. This small bonus pushes quick tasks up the list without overshadowing critical work.