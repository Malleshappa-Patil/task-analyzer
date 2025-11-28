### **Step 2: How to Run the Tests**

You don't run this file directly with `python`. You use Django's test runner.

1. Before running the tests, ensure your virtual environment is activated and all dependencies are installed.
# On mac us source venv/bin/activate  # On Windows use venn\Scripts\activate

2.  Open your terminal in the `backend/` folder.
3.  Run this command:

```bash
python manage.py test
```

### **What the Output Means**
You should see output that looks like this:

```text
Found 4 test(s).
Creating test database for alias 'default'...
....
----------------------------------------------------------------------
Ran 4 tests in 0.002s

OK
Destroying test database for alias 'default'...

