import logging

from django.core.management import BaseCommand

from scrapper.models import Profile, Site
from scrapper.service.client import client_factory
from scrapper.service.client.client_api import SuperjobApiClient
from scrapper.service.client.client_factory import CLIENT_SUPREJOB

log = logging.getLogger('console')


class Command(BaseCommand):
    help = "populates scanned profiles with additional data"

    BATCH_SIZE = SuperjobApiClient.BATCH_SIZE

    def handle(self, *args, **options):
        site = Site.objects.filter(title=CLIENT_SUPREJOB).first()
        client = client_factory.get_instance(site)
        scanned_ids = set(p.outer_id for p in Profile.objects.filter(scanned_at__isnull=False, site=site))
        cities_count = dict()

        while True:
            profile = Profile.objects.filter(scanned_at__isnull=True, site=site) \
                .exclude(outer_id__in=scanned_ids)\
                .exclude(segment__in=['Топ руководители', 'Рекламщики СМИ'])\
                .first()

            if not profile:
                break

            # TODO: временный костыль
            if profile.city not in cities_count:
                cities_count[profile.city] = 0
            elif cities_count[profile.city] > 500:
                scanned_ids.add(profile.outer_id)
                continue
            else:
                cities_count[profile.city] += 1

            client.api_populate_profiles(profile)
            scanned_ids.add(profile.outer_id)
