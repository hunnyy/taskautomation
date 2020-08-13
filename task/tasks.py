from celery import shared_task
from .models import *

@shared_task
def send_email_task(**kwargs):
	print('This is the update', kwargs)
	return None