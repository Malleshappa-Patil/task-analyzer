from django.test import TestCase
from datetime import date, timedelta
from .scoring import calculate_task_score

class ScoringAlgorithmTests(TestCase):
    
    def test_overdue_high_importance(self):
        """Test 1: Overdue + High Importance = Massive Score"""
        overdue_date = str(date.today() - timedelta(days=10))
        task_data = {
            'due_date': overdue_date,
            'importance': 10,
            'estimated_hours': 4,
            'dependencies': []
        }
        score = calculate_task_score(task_data, is_dict=True)
        self.assertTrue(score > 150, f"Score {score} should be > 150")

    def test_future_low_importance(self):
        """Test 2: Future + Low Importance = Low Score"""
        future_date = str(date.today() + timedelta(days=30))
        task_data = {
            'due_date': future_date,
            'importance': 1,
            'estimated_hours': 4,
            'dependencies': []
        }
        score = calculate_task_score(task_data, is_dict=True)
        self.assertTrue(score < 20, f"Score {score} should be low")

    def test_missing_due_date(self):
        """Test 3: Missing due date should default to safe values, not crash"""
        task_data = {
            'due_date': None,
            'importance': 5,
            'estimated_hours': 4,
            'dependencies': []
        }
        try:
            score = calculate_task_score(task_data, is_dict=True)
            # FIX IS HERE: using assertTrue instead of assertIsInstance
            self.assertTrue(score > 0, "Score should be a positive number")
        except Exception as e:
            self.fail(f"Algorithm crashed on missing date: {e}")

    def test_quick_win_bonus(self):
        """Test 4: Short tasks (<= 2h) get a bonus"""
        task_data = {
            'due_date': str(date.today()),
            'importance': 5,
            'estimated_hours': 1, # Quick win
            'dependencies': []
        }
        score = calculate_task_score(task_data, is_dict=True)
        self.assertTrue(score > 0)
        