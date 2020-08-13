from rest_framework import serializers
from .models import *

class TaskTrackerSerializer(serializers.ModelSerializer):
	class Meta:
		model = TaskTracker
		fields = ['task_type', 'email', 'update_type']

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model=Task
		fields = ['task_type', 'task_desc']
