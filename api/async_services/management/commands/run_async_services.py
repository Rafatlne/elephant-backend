from django.core.management.base import BaseCommand
from django_rq import get_queue

from api.async_services.services.all_author_execution import enqueue_call_api_tasks_for_all_authors
from api.async_services.services.contents_api_execution import execute_contents_api


class Command(BaseCommand):
    help = "Run Contest Execution"

    def handle(self, *args, **options):
        queue = get_queue("default")
        queue.enqueue(execute_contents_api)
        queue.enqueue(enqueue_call_api_tasks_for_all_authors)
        self.stdout.write(self.style.SUCCESS("Contest Execution bot enqueued"))
