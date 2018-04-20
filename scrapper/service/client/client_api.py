import json
import time

from requests import HTTPError
from requests import Response

from scrapper.models import Site, Task, RegionDict, Profile
from scrapper.service.requests import get, validate_response

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
        cities = [89, 42, 33, 130, 12, 13, 17, 119, 5, 173]
        segments = {
            # 'Рекламщики СМИ': {
            #     'keywords': [
            #         'Супервайзер отдела продаж',
            #         'Директор по продажам и развитию',
            #         'Директор по продажам',
            #         'Директор по развитию',
            #         'Менеджер по развитию',
            #         'Руководитель отдела',
            #         'Генеральный директор',
            #         'Руководитель группы',
            #         'Коммерческий директор',
            #         'Ведущий менеджер по продажам',
            #         'Руководитель направления',
            #         'Руководитель департамента',
            #         'Начальник отдела',
            #         'Заместитель руководителя',
            #         'Директор по продажам',
            #         'Специалист по работе с клиентами',
            #         'Директор по работе с клиентами',
            #         'Account manager',
            #         'Business development director',
            #         'Business development manager',
            #         'Аккаунт-менеджер',
            #         'Аккаунт-директор',
            #         'Региональный менеджер',
            #     ],
            #     'params': {
            #         'catalogues': ','.join([str(492)]),
            #         'payment_from': 30000,
            #         'age_from': 25,
            #         'age_to': 60,
            #     }
            # },
            # 'Страховой агент': {
            #     'keywords': [
            #         'Страховой агент',
            #         'Руководитель отдела страхования',
            #         'Специалист по страхованию',
            #         'Страховой консультант',
            #         'Страховой агент НПФ',
            #         'Страховой представителль',
            #         'Страховой брокер',
            #     ],
            #     'params': {
            #         'payment_from': 25000,
            #         'age_from': 25,
            #         'age_to': 60,
            #     }
            # },
            # 'Рано на пенсию': {
            #     'keywords': [
            #         'Учитель начальных классов',
            #         'Педагог',
            #         'летчик',
            #         'шахтер',
            #         'МЧС',
            #         'военный',
            #         'воспитатель',
            #         'воспитатель детского сада',
            #         'врач',
            #         'геолог',
            #         'гинеколог',
            #         'доктор',
            #         'железнодорожник',
            #         'крановщик',
            #         'криминалист',
            #         'машинист',
            #         'машинист крана',
            #         'машинист локомотива',
            #         'машинист поезда',
            #         'медсестра',
            #         'милиционер',
            #         'моряк',
            #         'нефтяник',
            #         'педагог',
            #         'пилот',
            #         'пожарный',
            #         'полицейский',
            #         'прокурор',
            #         'сварщик',
            #         'следователь',
            #         'спасатель',
            #         'стоматолог',
            #         'учитель',
            #         'фармацевт',
            #         'фельдшер',
            #         'воспитатель',
            #     ],
            #     'params': {
            #         'gender': 3,
            #         'age_from': 37,
            #     }
            # },
            # 'Топ руководители': {
            #     'keywords': [
            #         'Директор филиала',
            #         'Генеральный директор',
            #         'Индивидуальный предприниматель',
            #     ],
            #     'params': {
            #         'catalogues': ','.join(map(str, [499, 33, 11, 284, 493, 492, 471, 482, 438])),
            #         'age_from': 40,
            #     }
            # },
            'Сетевики MLM': {
                'keywords': [
                    'Представитель компании',
                    'Продавец-консультант',
                    'Консультант',
                ],
                'params': {
                    'gender': 3,
                    'age_from': 25,
                    'organizations': [
                        'Орифлэйм косметикс',
                        'Эйвон Бьюти Продак Компани',
                        'Avon',
                        'Amway',
                        # 'Biosea',
                        # 'Beautiful Life',
                        # 'Коралловый Клуб',
                        # 'CieAura  ',
                        # 'Си Аура',
                        # 'Colors of Life',
                        # 'Ciel Parfum  ',
                        # 'Си Эль Парфюм',
                        # 'Doctor Nona  ',
                        # 'Доктор Нона',
                        # 'Essens',
                        # 'Energetix  Энергетикс',
                        # 'eCosway',
                        # 'Farmasi  Фармаси',
                        # 'Fleur de Sante',
                        # 'Faberlic  Фаберлик',
                        # 'FFI',
                        # 'Fm Group  ФМ Групп',
                        # 'ForeverLiving Product  ',
                        # 'Форевер Ливинг',
                        # 'Fohow',
                        # 'FDM Club',
                        # 'Gtime',
                        # 'Gloryon',
                        # 'Green World  ',
                        # 'Грин Ворлд',
                        # 'GRS',
                        # 'Greenfoot Global  Envirotabs',
                        # 'Herbalife  ',
                        # 'Гербалайф',
                        # 'Hao Gang  ',
                        # 'Хао Ган',
                        # 'I-Top',
                        # 'Jeunesse Global',
                        # 'Kyani ',
                        # 'Каяни',
                        # 'Lambre',
                        # ' Ламбре',
                        # 'LR Health And Beauty Systems',
                        # 'Monavie',
                        # 'Mageric ',
                        # 'Маджерик',
                        # 'Mirra',
                        # 'Мирра',
                        # 'Neways',
                        # 'Ньювейс',
                        # 'Nht Global',
                        # 'Nikken  ',
                        # 'Никкен',
                        # 'Nl International  ',
                        # 'Нл Интернешнл',
                        # 'Nu Skin',
                        # 'NWA',
                        # 'NSP',
                        # 'Oriflame  ',
                        # 'Орифлейм',
                        # 'Organo Gold',
                        # 'Qnet',
                        # 'QwertyPAY',
                        # 'Ra Group  ',
                        # 'Ра Групп',
                        # 'Santegra',
                        # 'Sigcess',
                        # 'Silkway',
                        # 'Sisel',
                        # 'SkinnyBodyCare',
                        # 'Stemtech',
                        # 'Tiens ',
                        # 'Тяньши',
                        # 'Tahitian Noni International',
                        # 'Tiande ',
                        # 'Тианде',
                        # 'Tupperware ',
                        # 'Тапервер',
                        # 'Unhwa  Унхва',
                        # 'Vis Energy',
                        # 'Vilavi  Вилави',
                        # 'Venera.Beauty Home ',
                        # 'Венера Бьюти Хоум',
                        # 'Vitaline ',
                        # 'Виталайн',
                        # 'Vision ',
                        # 'Визион',
                        # 'Vivasan',
                        # 'Вивасан',
                        # 'Winalite ',
                        # 'Виналайт',
                        # 'Xango',
                        # 'Zepter ',
                        # 'Цептер',
                        # 'Автоклуб (Международный Автоклуб)',
                        # 'Амрита',
                        # 'Аромашарм',
                        # 'Арго',
                        # 'Арт Лайф',
                        # 'Асония',
                        # 'Аксиомия',
                        # 'Бинг Хан',
                        # 'Бонус Лайф',
                        # 'Биомедис',
                        # 'Батель',
                        # 'Витамакс',
                        # 'Глорион',
                        # 'ДЭНАС',
                        # 'ДЕТА-ЭЛИС',
                        # 'Дайна',
                        # 'Едоша',
                        # 'Коралловый Клуб',
                        # 'Мейтан',
                        # 'Новая Эра',
                        # 'ННПЦТО',
                        # 'НПЦРиЗ',
                        # 'Омегавит',
                        # 'Сибирское Здоровье',
                        # 'Тенториум',
                        # 'Фермион',
                        # 'Центр Регион',
                        # 'Эскалат',
                        # 'Эковита',
                        # 'Ялма',
                        # 'Desheli',
                        # 'Sun Way',
                        # 'Вертера Органик',
                        # 'NHC Living',
                        # 'Bottega Verde',
                        # 'Fucoidan World',
                        # 'Armelle',
                        # 'JafraДжафра',
                        # 'Ипар',
                        # 'LuckLife',
                        # 'Perfect Organics',
                        # 'Флоранж',
                        # 'Deesse',
                        # 'Prana Food',
                        # 'TopLife',
                        # 'САД',
                        # 'J’erelia',
                        # 'Лавилайтс',
                        # 'Белый Кот',
                        # 'Mary Kay',
                        # '4life Research',
                        # 'Альфа Эра',
                        # 'Litani',
                        # 'Riway',
                        # 'ЛиВест',
                    ]
                }
            },
        }

        for city in cities:
            for segment_name, segment in segments.items():
                for keyword in segment.get('keywords'):
                    self.api_search(task, city, keyword, segment_name, segment.get('params'))

    def api_search(self, task: Task, city_id: int, keyword: str, segment: str, search_params: dict) -> None:
        profile_counter = 0
        params = {
            # 'keyword': task.keyword,
            'page': 0,
            'count': 100,
            'keyword': keyword,             # сделать через таску
            't[]': {city_id},                # сделать через таску
            'citizenship[]': {1},
        }

        if search_params.get('catalogues'): params['catalogues'] = search_params.get('catalogues')
        if search_params.get('payment_from'): params['payment_from'] = search_params.get('payment_from')
        if search_params.get('age_from'): params['age_from'] = search_params.get('age_from')
        if search_params.get('age_to'): params['age_to'] = search_params.get('age_to')
        if search_params.get('gender'): params['gender'] = search_params.get('gender')
        if search_params.get('organizations'):
            params['keywords[0][srws]'] = '8'
            params['keywords[0][keys]'] = search_params.get('organizations')
            params['keywords[0][skwc]'] = 'or'

        # if task.search_params:
        #     search_params = json.load(task.search_params)
        #     if 'town_id' in search_params: params['t[]'] = dict(search_params.get('town_id'))
        #     if 'region_id' in search_params: params['r[]'] = dict(search_params.get('region_id'))

        while True:
        # while profile_counter < task.limit:
            response = get(self.URL_RESUMES_SEARCH, params=params, headers=self.api_headers)

            if not validate_response(response, self.errors):
                raise HTTPError(str(self.errors))

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
                    keyword=keyword,
                    task=task,
                    segment=segment,
                ).save()
                profile_counter += 1

            if not response_json.get('more', False):
                break
            else:
                params['page'] += 1

        # task.save()

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

        if not validate_response(response, self.errors):
            raise HTTPError(str(self.errors))

        response_json = response.json()
        self.access_token = response_json['access_token']
        self.refresh_token = response_json['refresh_token']
        self.token_valid_till = int(response_json['ttl'])

    def api_deep_search(self, outer_ids: [int]) -> None:
        pass


