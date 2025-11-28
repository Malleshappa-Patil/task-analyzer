import requests
import json
import sys

# Base URL of your local Django server
BASE_URL = "http://127.0.0.1:8000/api/tasks"

def run_manual_check():
    print("--- Running Manual Verification Script ---")
    
    # Define dummy data
    payload = [
        {
            "title": "Manual Check: Overdue Task", 
            "due_date": "2023-01-01", 
            "estimated_hours": 2, 
            "importance": 10, 
            "dependencies": []
        },
        {
            "title": "Manual Check: Future Task", 
            "due_date": "2030-01-01", 
            "estimated_hours": 2, 
            "importance": 1, 
            "dependencies": []
        }
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/analyze/", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            results = response.json()
            print("\nAPI is reachable and logic is working!")
            print(f"Top Task Score: {results[0]['priority_score']} (Should be high)")
            print(f"Bottom Task Score: {results[1]['priority_score']} (Should be low)")
        else:
            print(f"Error: {response.status_code}")

    except Exception as e:
        print(f"Connection Failed: {e}")
        print("Ensure 'python manage.py runserver' is running!")

if __name__ == "__main__":
    try:
        import requests
        run_manual_check()
    except ImportError:
        print("Please run: pip install requests")
