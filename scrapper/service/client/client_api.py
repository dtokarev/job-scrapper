import json
import time

from requests import HTTPError

from scrapper.models import Site, Task, Profile
from scrapper.service.requests import get, validate_response


def get_site(title):
    return Site.objects.filter(title=title).first()


class SuperjobApiClient:
    URL_RETURN = 'http://www.ex.ru'
    URL_API = 'https://api.superjob.ru/2.0/'
    URL_OAUTH_AUTHORIZE = 'http://www.superjob.ru/authorize'
    URL_TOKEN = URL_API+'oauth2/password/'
    URL_REFRESH = URL_API+'oauth2/refresh_token/'
    URL_RESUMES_SEARCH = URL_API+'resumes/'

    def __init__(self, site):
        super().__init__()
        self.site = site
        self.errors = list()
        self.code = ''
        self.access_token = ''
        self.refresh_token = ''
        self.token_valid_till = time.time()

    def parse(self, task: Task) -> None:
        print('----------')
        # self.refresh_credentials()
        self.api_search(task)

    def api_search(self, task: Task) -> None:
        profiles_scanned = 0
        params = self.build_search_params(task)
        api_headers = {'X-Api-App-Id': self.site.app_secret, 'Content-Type': 'application/x-www-form-urlencoded'}

        while profiles_scanned < task.limit:
            response = get(self.URL_RESUMES_SEARCH, params=params, headers=api_headers)

            if not validate_response(response, self.errors):
                return

            response_json = response.json()
            task.total_found = response_json.get('total', 0)

            print(task.total_found)

            for p in response_json.get('objects', []):
                Profile(
                    site=self.site,
                    link=p.get('link', ''),
                    outer_id=p.get('id_user', ''),
                    name=p.get('firstname', ''),
                    lastname=p.get('lastname', ''),
                    email=p.get('email', ''),
                    city=p.get('town', {}).get('title', ''),
                    info=str(p),
                    keyword=task.keyword,
                    task=task,
                    segment=task.segment,
                ).save()
                profiles_scanned += 1

            if not response_json.get('more', False):
                break
            else:
                params['page'] += 1

    @staticmethod
    def build_search_params(task: Task) -> dict:
        params = {
            'page': 0,
            'count': 100,
            'citizenship[]': {1},
            'keyword': task.keyword
        }

        if task.search_params:
            search_params = json.loads(task.search_params)
            if search_params.get('town_id'):
                params['t[]'] = [search_params.get('town_id'), ]
            if search_params.get('region_id'):
                params['r[]'] = [search_params.get('region_id'), ]
            if search_params.get('specialization'):     #сделать словарь
                params['catalogues'] = search_params.get('specialization')
            if search_params.get('payment_from'):
                params['payment_from'] = search_params.get('payment_from')
            if search_params.get('age_from'):
                params['age_from'] = search_params.get('age_from')
            if search_params.get('age_to'):
                params['age_to'] = search_params.get('age_to')
            if search_params.get('gender'):         #сделать словарь 2-муж, 3-жен
                params['gender'] = search_params.get('gender')
            if search_params.get('and_keywords'):
                # params['keywords[0][srws]'] = '7'
                # params['keywords[0][skwc]'] = 'and'
                # params['keywords[0][keys]'] = task.keyword
                params['keywords[1][srws]'] = '7'
                params['keywords[1][skwc]'] = 'or'
                params['keywords[1][keys][]'] = search_params.get('and_keywords')
            # else:
            #     params['keyword'] = task.keyword
        return params

    def refresh_credentials(self) -> None:
        if self.token_valid_till - time.time() > 10:
            return

        # обновляем или генерим новый
        has_token = '' not in (self.code, self.access_token, self.refresh_token)
        params = {'client_id': self.site.app_id, 'client_secret': self.site.app_secret, 'hr': 1}
        if has_token:
            params.update({'refresh_token': self.refresh_token})
            token_url = self.URL_REFRESH
        else:
            params.update({'login': self.site.login, 'password': self.site.password})
            token_url = self.URL_TOKEN
        response = get(token_url, params=params, json=False)

        if not validate_response(response, self.errors):
            raise HTTPError(str(self.errors))

        response_json = response.json()
        self.access_token = response_json['access_token']
        self.refresh_token = response_json['refresh_token']
        self.token_valid_till = int(response_json['ttl'])

    def api_deep_search(self, outer_ids: [int]) -> None:
        pass


