import logging

from django.core.management import BaseCommand
from django.db.models import Q

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
        scanned_ids = set(p.outer_id for p in Profile.objects.filter(email__isnull=False, site=site).exclude(email=''))

        while True:
            profiles = Profile.objects.filter(Q(email__isnull=True) | Q(email=''), site=site) \
                .exclude(outer_id__in=scanned_ids)[:self.BATCH_SIZE]
            if not profiles:
                break

            client.api_populate_profiles(profiles)

            for profile in profiles:
                print(profile.id)
                scanned_ids.add(profile.outer_id)

            break  # for test

