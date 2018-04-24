import logging

from django.core.management import BaseCommand
from django.db import transaction
from django.utils.timezone import now

from scrapper.models import Task
from scrapper.service.client import client_factory

log = logging.getLogger('console')


class Command(BaseCommand):
    help = "parse tasks in queue"

    @transaction.atomic
    def handle(self, *args, **options):
        tasks = Task.objects.filter(status=False, scanned_at__isnull=True).all()

        if not tasks:
            log.warning("no task found")
            return

        for task in tasks:
            task.status = Task.STATUS_IN_QUEUE
            task.save()

            client = client_factory.get_instance(task.site)
            client.parse(task)

            if client.errors:
                # TODO: uncomment
                # task.status = Task.STATUS_ERROR
                # task.scanned_at = now()
                task.errors = str(client.errors)
            else:
                task.status = Task.STATUS_COMPLETED
                task.scanned_at = now()

            task.save()


