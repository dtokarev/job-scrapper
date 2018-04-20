import logging

from django.core.management import BaseCommand
from requests import HTTPError

from scrapper.models import RegionDict, Site
from scrapper.service.client.client_api import SuperjobApiClient, CLIENT_SUPREJOB
from scrapper.service.requests import get

log = logging.getLogger('console')

URL_REGIONS = SuperjobApiClient.URL_API + 'regions/combined/'


class Command(BaseCommand):
    help = "Sync regions"

    def handle(self, *args, **options):
        self.sync_regions()

    def sync_regions(self) -> None:
        response = get(URL_REGIONS)
        json = response.json()

        if response.status_code > 400 or json is None:
            raise HTTPError

        site = Site.objects.filter(title=CLIENT_SUPREJOB).first()
        # удаляем что есть
        RegionDict.objects.filter(site=site).all().delete()
        # только Россия
        country = json[0]

        country_id = int(country['id'])
        country_name = country['title']

        self.save_town(country, site, country_id, country_name)
        if 'regions' in country:
            for region in country['regions']:
                self.save_town(region, site, country_id, country_name, region['id'], region['title'])

    @staticmethod
    def save_town(json, site, country_id, country_name, region_id=None, region_name=None):
        if 'towns' in json:
            for town in json['towns']:
                region = RegionDict(site=site, country_id=country_id, country_name=country_name)
                region.region_id = region_id if region_id is not None else int(town['id_region'])
                region.region_name = region_name if region_name is not None else town['title']
                region.town_id = int(town['id'])
                region.town_name = town['title']
                region.save()
