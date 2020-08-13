from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from .serializers import *

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
		if serializer.is_valid():
			serializer.save()
			return Response({'status':'SUCCESS', 'data':serializer.data})
		except Exception as e:
			return Response({'status' : 'ERROR', 'message':str(e)})

	def delete(self, request, pk):
		data=request.POST
		task=Task.objects.get(id=pk)
		task.delete()
		return Response({'status':'SUCCESS, Task Deleted'})

	def put(self, request, pk):
		data=request.POST
		task = Task.objects.get(id=pk)
		serializer = TaskSerializer(data=data)
		if serializer.is_valid():
			tasktype=serializer.data.get('task_type')
			taskdesc=serializer.data.get('task_desc')
			Task.task_type=tasktype
			Task.task_desc=taskdesc
			Task.save()
			return Response({'status':'SUCCESS'})
		return Response({'status':'ERROR', 'message':serializer.errors}) 


