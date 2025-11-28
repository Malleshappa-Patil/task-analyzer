### How to run the manual_test.py

## Step 1: Ensure the Server is Running
``` bash
# On mac use source venv/bin/activate 
# On Windows use: venn\Scripts\activate
cd backend
python manage.py runserver
```

## Step 2: Run the Manual Test
``` bash
cd task_analyzer
# On mac use: source venv/bin/activate
# On Windows use: venn\Scripts\activate
python manual_test.py
```

## Expected Output
--- Running Manual Verification Script ---

API is reachable and logic is working!
Top Task Score: 156.0 (Should be high)
Bottom Task Score: 9.5 (Should be low)
