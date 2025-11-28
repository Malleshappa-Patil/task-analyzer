from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=200)
    # Allowing null for due_date to handle "missing data" edge case [cite: 36]
    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.FloatField(
        validators=[MinValueValidator(0.1)]
    )
    importance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="1-10 scale"
    )
    # Recursive relationship: A task can depend on other tasks
    dependencies = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        blank=True,
        related_name='blocking'
    )
    
    # Store the calculated score so we don't have to re-calc every time (Optional but good for performance)
    priority_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if not self.due_date:
            return False
        return self.due_date < timezone.now().date()