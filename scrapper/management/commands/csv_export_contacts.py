import csv
import logging

from django.core.management import BaseCommand
from django.utils.timezone import now

from app.settings import BASE_DIR
from scrapper.models import Profile

log = logging.getLogger('console')


class Command(BaseCommand):
    help = "export contacts"
    FROM_TASK_ID = 3575

    def handle(self, *args, **options):
        file_path = '{}/files/csv/export_contacts_{}.csv'.format(BASE_DIR, now())
        profiles = Profile.objects.filter(scanned_at__isnull=False, task_id__gte=Command.FROM_TASK_ID).all()

        with open(file_path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['name', 'lastname', 'link', 'email', 'email provider',
                             'phone', 'segment', 'search key', 'city', 'duplicate'])
            for profile in profiles:
                writer.writerow([
                    profile.name,
                    profile.lastname,
                    profile.link,
                    profile.email,
                    profile.email_provider,
                    profile.phone,
                    profile.segment,
                    profile.keyword,
                    profile.city,
                    profile.duplicate
                ])


