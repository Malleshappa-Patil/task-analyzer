import requests
import json
import sys

# Base URL of your local Django server
BASE_URL = "http://127.0.0.1:8000/api/tasks"

def test_algorithm():
    print("--- 🧪 Testing Smart Task Algorithm ---")
    
    # 1. Define dummy data (Mixed priorities)
    # We expect: 
    #   1. "Fix Critical Bug" (Overdue + High Importance) -> HIGHEST
    #   2. "Write Report" (Due Today) -> MIDDLE
    #   3. "Plan Party" (Future + Low Importance) -> LOWEST
    
    payload = [
        {
            "title": "Plan Party", 
            "due_date": "2025-12-25", 
            "estimated_hours": 5, 
            "importance": 3, 
            "dependencies": []
        },
        {
            "title": "Fix Critical Bug", 
            "due_date": "2023-01-01",  # Intentionally in the past
            "estimated_hours": 2, 
            "importance": 10, 
            "dependencies": []
        },
        {
            "title": "Write Report", 
            "due_date": "2025-11-29", # Assume this is "Soon/Today" relative to context
            "estimated_hours": 1, 
            "importance": 7, 
            "dependencies": []
        }
    ]

    try:
        # 2. Send POST request to /analyze/
        response = requests.post(
            f"{BASE_URL}/analyze/", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            results = response.json()
            print("\n✅ API Success! Here is the Prioritized List:\n")
            for i, task in enumerate(results, 1):
                print(f"{i}. Score: {task['priority_score']} | Task: {task['title']}")
                print(f"   (Due: {task['due_date']}, Imp: {task['importance']})")
                print("-" * 40)
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        print("Make sure 'python manage.py runserver' is running in another terminal!")

if __name__ == "__main__":
    # Ensure 'requests' is installed
    try:
        import requests
        test_algorithm()
    except ImportError:
        print("Please run: pip install requests")