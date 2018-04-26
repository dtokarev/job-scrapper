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
        city_segment_count = dict()

        while True:
            profile = Profile.objects.filter(scanned_at__isnull=True, site=site) \
                .exclude(outer_id__in=scanned_ids)\
                .first()

            if not profile:
                break

            # TODO: временный костыль
            key = '{}{}'.format(profile.segment, profile.city)
            if key not in city_segment_count:
                city_segment_count[key] = 0
            elif city_segment_count[key] > 200:
                scanned_ids.add(profile.outer_id)
                continue
            else:
                city_segment_count[key] += 1

            print('{}: {}'.format(key, city_segment_count[key]))

            client.api_populate_profiles(profile)
            scanned_ids.add(profile.outer_id)
