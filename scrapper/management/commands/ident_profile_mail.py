import logging

from django.core.management import BaseCommand

from scrapper.models import Profile
from scrapper.service.profile_service import ident_provider

log = logging.getLogger('console')


class Command(BaseCommand):
    help = "mail company by domain"

    # @transaction.atomic
    def handle(self, *args, **options):

        profiles = Profile.objects\
            .filter(email_provider__isnull=True, email__isnull=False)\
            .exclude(email='')\
            .all()

        for profile in profiles:
            profile.email_provider = ident_provider(profile.email)
            profile.save()
            print('{} saved'.format(profile.id))



