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