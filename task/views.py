from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from .serializers import *
from .tasks import send_email_task
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import datetime
import pytz


class TaskApi(APIView):
	def get(self, request):
		try:
			queryset = Task.objects.all()
			serializer = TaskSerializer(queryset, many=True)
			return Response({'status':'SUCCESS', 'data':serializer.data})
		except Exception as e:
			return Response({'status' : 'ERROR', 'message':str(e)})

	def post(self, request):
		data = request.POST
		serializer = TaskSerializer(data=data, partial=True)
		try:
			if serializer.is_valid():
				serializer.save()
				return Response({'status':'SUCCESS', 'data':serializer.data})
			else:
				return Response({'status':'ERROR', 'message': 'Task type is not valid'})
		except Exception as e:
			return Response({'status' : 'ERROR', 'message':str(e)})


class TaskUpdateApi(APIView):
	def put(self, request, pk):
		data=request.POST
		task = Task.objects.get(id=pk)
		serializer = TaskSerializer(task,data=data)
		if serializer.is_valid():
			serializer.save()
			return Response({'status':'SUCCESS, Task is updated'})
		return Response({'status':'ERROR', 'message':serializer.errors}) 

class TaskDeleteApi(APIView):
	def delete(self, request, pk):
		try:
			data=request.POST
			task=Task.objects.get(id=pk)
			task.delete()
			return Response({'status':'SUCCESS, Task Deleted'})
		except Exception as e:
			return Response({'status' : 'ERROR', 'message':str(e)})

class TaskTrackerApi(APIView):
	def get(self, request):
		queryset = TaskTracker.objects.all()
		try:
			serializer = TaskTrackerSerializer(queryset, many=True)
			return Response({'status':'SUCCESS', 'data':serializer.data})
		except Exception as e:
			return Response({'status' : 'ERROR', 'message':str(e)})

	def post(self, request):
		data = request.POST
		serializer = TaskTrackerSerializer(data=data, partial=True)
		try:
			if serializer.is_valid():
				u_type=data.get('update_type')
				if u_type == 'Weekly':
					name = data.get('email')
					schedule, _ = CrontabSchedule.objects.get_or_create(day_of_week='monday', timezone=pytz.timezone('Asia/Kolkata'))
					mailtask = PeriodicTask.objects.create(crontab=schedule,name=name,task='task.tasks.send_email_task', start_time=datetime.datetime.now(), kwargs=json.dumps({'id':'task'}))
					schedule.save()
					mailtask.save()

				elif u_type == 'Daily':
					name = data.get('email')
					schedule, _ = CrontabSchedule.objects.get_or_create(minute=00, hour=17, timezone=pytz.timezone('Asia/Kolkata'))
					mailtask = PeriodicTask.objects.create(crontab=schedule,name=name,task='task.tasks.send_email_task', start_time=datetime.datetime.now(), kwargs=json.dumps({'id':'task'}))
					schedule.save()
					mailtask.save()
				elif u_type == 'Monthly':
					name = data.get('email')
					schedule, _ = CrontabSchedule.objects.get_or_create(minute=0, hour=0, day_of_month='1', timezone=pytz.timezone('Asia/Kolkata'))
					mailtask = PeriodicTask.objects.create(crontab=schedule,name=name,task='task.tasks.send_email_task', start_time=datetime.datetime.now(), kwargs=json.dumps({'id':'task'}))
					schedule.save()
					mailtask.save()
				
				serializer.save()
				return Response({'status':'SUCCESS', 'data':serializer.data})
			else:
				return Response({'status':'ERROR', 'message': 'This email ID you entered have been used before. Please use a different email, or Task you selected does not exists, or Not Valid Update Type!'})
		except Exception as e:
			return Response({'status' : 'ERROR', 'message':str(e)})

