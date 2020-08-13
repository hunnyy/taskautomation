from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Task(models.Model):
	
	class Type(models.IntegerChoices):
		TASK1 = 1
		TASK2 = 2
		TASK3 = 3
		TASK4 = 4

	task_type = models.IntegerField(choices=Type.choices)
	task_desc = models.CharField(max_length=1000)

class TaskTracker(models.Model):

	Type = (
	('Weekly', 'Weekly'),
	('Daily', 'Daily'),
	('Monthly', 'Monthly'),
	)

	task_type = models.ForeignKey(Task, on_delete=models.CASCADE, unique=False)
	email = models.EmailField(_('email address'), unique=True)
	update_type = models.CharField(choices=Type, max_length=15)