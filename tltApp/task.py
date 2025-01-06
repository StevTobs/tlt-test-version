# your_app/tasks.py

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time

@shared_task
def long_running_task():
    channel_layer = get_channel_layer()
    for i in range(101):
        # Simulate work
        time.sleep(0.1)
        # Send progress update
        async_to_sync(channel_layer.group_send)(
            'progress_updates',
            {
                'type': 'progress.update',
                'message': i,
            }
        )
    return "Task Completed"
