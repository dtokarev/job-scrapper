from urllib.parse import urlencode
from bs4 import BeautifulSoup
from scrapper.models import Site, Profile, Task
from scrapper.service import requests

BS_PARSER = 'lxml'


class JobstreetCrawler:
    URL_SEARCH = 'https://www.jobstreet.com.ph/en/job-search/job-vacancy.php?key={' \
                 'keyword}&area=1&specialization=135&experience-min=-1&experience-max=-1&salary=1%2C000&salary-option' \
                 '=on&job-posted=0&src=1&ojs=4'

    def parse(self):
        pass


class HHCrawler:
    URL_SEARCH = 'https://hh.ru/search/resume?'

    def __init__(self, site: Site):
        super().__init__()
        self.site = site

    def parse(self, task: Task):
        page = 0
        total = 0
        while True:
            url = self.build_search_url({}, "Business development manager", page)
            response = requests.get(url)
            bs = BeautifulSoup(response, BS_PARSER)
            if not total:
                total = self.count_pages(bs)
            links = self.get_links(bs)

            for link in links:
                profile = Profile()
                self.fill_profile(profile, link)
                profile.save()

            if page >= total:
                break

    def build_search_url(self, params, keyword, page):
        # заменить на Task
        p = {
            'order_by': 'relevance',
            'area': 1,
            'text': keyword,
            'logic': 'normal',
            'pos': 'full_text',
            'exp_period': 'all_time',
            'clusters': True,
            'page': page
        }
        labels = set()

        if params.get('age_from'):
            p.update(params.get('age_from'))
            labels.add('only_with_age')
        if params.get('age_to'):
            p.update(params.get('age_to'))
            labels.add('only_with_age')
        if params.get('salary_from'):
            p.update(params.get('salary_from'))
            labels.add('only_with_salary')
        if params.get('salary_to'):
            p.update(params.get('salary_to'))
            labels.add('only_with_salary')
        if params.get('salary_from'):
            p.update(params.get('salary_from'))
            labels.add('only_with_salary')
        if params.get('gender'):
            p.update(params.get('gender'))
            labels.add('only_with_gender')
        if params.get('specialization'):
            p.update(params.get('specialization'))
            p.update({'from': 'cluster_professionalArea'})

        url = self.URL_SEARCH + urlencode(p)

        if labels:
            url += '&label='+'&label='.join(labels)

        return url

    @staticmethod
    def count_pages(bs: BeautifulSoup)-> int:
        links = bs.find_all('a', attrs={'class': 'HH-Pager-Control'})
        if not links:
            return 0

        return int(links[-1].get_text())-1

    @staticmethod
    def get_links(bs: BeautifulSoup) -> list():
        return bs.find_all('a', attrs={'itemprop': 'jobTitle'})

    @staticmethod
    def fill_profile(profile: Profile, url):
        pass
