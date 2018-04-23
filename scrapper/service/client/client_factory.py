from scrapper.service.client.client_api import *
from scrapper.service.client.client_crawler import *

CLIENT_SUPREJOB = 'SUPREJOB'
CLIENT_JOBSTREET = 'JOBSTREET'
CLIENT_HH = 'HH'


def get_instance(site: Site):
    if site.title == CLIENT_SUPREJOB:
        return SuperjobApiClient(site)
    if site.title == CLIENT_JOBSTREET:
        pass
        # return JobstreetCrawler(site)
    if site.title == CLIENT_HH:
        return HHCrawler(site)
