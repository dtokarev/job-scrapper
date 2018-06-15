import logging

from django.core.management import BaseCommand
from django.utils.timezone import now

from app.settings import BASE_DIR
from scrapper.models import Profile
from scrapper.service.csv import dict_to_csv

log = logging.getLogger('console')


class Command(BaseCommand):
    help = "city / segment matrix"
    FROM_TASK_ID = 3575

    def handle(self, *args, **options):
        profiles = Profile.objects.filter(email_provider__isnull=False, task_id__gte=Command.FROM_TASK_ID).all()

        # 2 dim dictionary from all records
        m = {}
        for profile in profiles:
            if profile.segment in m and profile.city in m[profile.segment]:
                m[profile.segment][profile.city] += 1
            else:
                if profile.segment not in m:
                    m[profile.segment] = dict()
                m[profile.segment].update({profile.city: 1})

        dict_to_csv(m,  '{}/files/csv/by_segment_{}.csv'.format(BASE_DIR, now()))

