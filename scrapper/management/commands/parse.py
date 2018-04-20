import logging

from django.core.management import BaseCommand

from scrapper.models import Task
from scrapper.service.client.client_api import SuperjobApiClient

log = logging.getLogger('console')


class Command(BaseCommand):
    help = "My command"

    def handle(self, *args, **options):
        tasks = Task.objects.filter(in_process=False, scanned_at__isnull=True).all()

        # if not tasks:
        #     log.warning("no task found")
        #     return

        client = SuperjobApiClient()
        client.parse(tasks.first())
        # for task in tasks:
        #     client = SuperjobClient()
        #     log.error(client.login())
