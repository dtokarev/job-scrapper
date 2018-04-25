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
        scanned_ids = set()

        while True:
            profiles = Profile.objects.filter(site=site, email__isnull=False) \
                .exclude(resume_id__in=scanned_ids, email='')[:self.BATCH_SIZE]
            if not profiles:
                break

            for profile in profiles:
                scanned_ids.add(profile.outer_id)

            client.api_populate_profiles(profiles)
