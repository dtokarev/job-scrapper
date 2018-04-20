import json
import time

from requests import HTTPError
from requests import Response

from scrapper.models import Site, Task, RegionDict, Profile
from scrapper.service.requests import get


CLIENT_SUPREJOB = 'SUPREJOB'


def get_site(title):
    return Site.objects.filter(title=title).first()


class SuperjobApiClient:
    site = get_site(CLIENT_SUPREJOB)

    APP_LOGIN = site.login
    APP_PASSWORD = site.password
    APP_ID = site.app_id
    APP_SECRET = site.app_secret

    URL_RETURN = 'http://www.ex.ru'
    URL_API = 'https://api.superjob.ru/2.0/'
    URL_OAUTH_AUTHORIZE = 'http://www.superjob.ru/authorize'
    URL_TOKEN = URL_API+'oauth2/password/'
    URL_REFRESH = URL_API+'oauth2/refresh_token/'
    URL_RESUMES_SEARCH = URL_API+'resumes/'

    api_headers = {
        'X-Api-App-Id': APP_SECRET,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def __init__(self):
        super().__init__()
        self.errors = list()
        self.code = ''
        self.access_token = ''
        self.refresh_token = ''
        self.token_valid_till = time.time()

    def parse(self, task: Task) -> None:
        print('----------')
        # self.refresh_credentials()
        self.api_search(task)
        print('----------')

    def refresh_credentials(self) -> None:
        if self.token_valid_till - time.time() > 10:
            return

        # обновляем или генерим новый
        has_token = '' not in (self.code, self.access_token, self.refresh_token)
        params = {'client_id': self.APP_ID, 'client_secret': self.APP_SECRET, 'hr': 1}
        if has_token:
            params.update({'refresh_token': self.refresh_token})
            token_url = self.URL_REFRESH
        else:
            params.update({'login': self.APP_LOGIN, 'password': self.APP_PASSWORD})
            token_url = self.URL_TOKEN
        response = get(token_url, params=params, json=False)

        if not self.validate_response(response):
            raise HTTPError(str(self.errors))

        json = response.json()
        self.access_token = json['access_token']
        self.refresh_token = json['refresh_token']
        self.token_valid_till = int(json['ttl'])

    def api_search(self, task: Task):
        profile_counter = 0
        params = {
            'keyword': task.keyword,
            'page': 0,
            'count': 10
        }

        if task.search_params:
            search_params = json.load(task.search_params)
            if 'town_id' in search_params: params['t[]'] = dict(search_params.get('town_id'))
            if 'region_id' in search_params: params['r[]'] = dict(search_params.get('region_id'))

        while profile_counter < task.limit:
            response = get(self.URL_RESUMES_SEARCH, params=params, headers=self.api_headers)

            if not self.validate_response(response):
                raise HTTPError(str(self.errors))

            r_json = response.json()
            task.total_found = r_json.get('total', 0)

            for p in r_json().get('objects', []):
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
                    segment=1,
                ).save()
                profile_counter += 1
            params['page'] += 1
        task.save()

    def validate_response(self, response: Response) -> bool:
        if int(response.status_code) < 400:
            return True
        self.errors.append(str(response.json()))

        return False

