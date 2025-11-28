from datetime import datetime, date
from django.utils import timezone

def calculate_task_score(task_data, is_dict=False):
    """
    Calculates the priority score based on the 'Smart Balance' algorithm.
    S = Urgency + (Importance * 5) + Dependencies + Effort
    """
    
    # 1. Normalize Data (Handle Dict vs Object)
    if is_dict:
        due_date_str = task_data.get('due_date')
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        else:
            due_date = None
        importance = task_data.get('importance', 5)
        hours = task_data.get('estimated_hours', 4)
        # Note: Dependency counting for raw JSON is hard without context. 
        # We will assume 0 for raw JSON or require pre-calculation.
        dependency_count = len(task_data.get('dependencies', [])) 
    else:
        # It is a Django Model Object
        due_date = task_data.due_date
        importance = task_data.importance
        hours = task_data.estimated_hours
        # For DB objects, we want tasks that rely on THIS task (blocking power)
        dependency_count = task_data.blocking.count()

    # --- THE ALGORITHM ---

    score = 0
    
    # A. Urgency Score
    if due_date:
        today = timezone.now().date()
        delta = (due_date - today).days
        
        if delta < 0: # Overdue
            score += 100 + (abs(delta) * 2)
        elif delta == 0: # Due Today
            score += 75
        elif delta <= 2: # Due Soon
            score += 50
        elif delta <= 7: # This Week
            score += 25
        else: # Future
            score += 10 - (delta * 0.5)
    else:
        score += 10 # No due date = Low urgency

    # B. Importance Score (Weight: 5x)
    score += (importance * 5)

    # C. Dependency Score (Bottleneck Factor)
    # If this task blocks 2 others, it's very important to clear.
    score += (dependency_count * 10)

    # D. Effort Score (Quick Wins)
    if hours <= 2:
        score += 10 # Quick win bonus
    elif hours >= 10:
        score -= 5 # Large task penalty (encourage breakdown)

    return round(score, 2)