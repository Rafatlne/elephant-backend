# tasks.py
import time
from datetime import datetime, timedelta

from django.utils import timezone
from rq import get_current_job
from django_rq import job, get_queue

from .author_api_execution import execute_author_api
from ...social_media.models import Author


@job('default', timeout='2m')
def enqueue_call_api_tasks_for_all_authors():
    # Get all authors from the database
    all_authors = Author.objects.all()
    default_queue = get_queue("default")
    now = timezone.now()
    check_at_30sec = now + timedelta(seconds=30)
    check_at_30min = now + timedelta(seconds=1800)

    # Iterate through each author and enqueue the call_api_task
    for author in all_authors:
        # Enqueue the job for each author
        execute_author_api(author.unique_id)
        time.sleep(30)

        # Introduce a delay between enqueuing jobs (if needed)

    # Log the completion time
    default_queue.enqueue_at(check_at_30min, enqueue_call_api_tasks_for_all_authors)
    print(f"Job completed at")
