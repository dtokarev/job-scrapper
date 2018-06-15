import json
import logging

from django.core.management import BaseCommand

from scrapper.models import Task, Site
from scrapper.service.client.client_factory import *

log = logging.getLogger('console')


class Command(BaseCommand):
    help = "add new task to queue"

    def handle(self, *args, **options):
        cities = [89, 42, 33, 130, 12, 13, 17, 119, 5, 173, 73, 55]

        tasks = {
            'Рекламщики СМИ': {
                'keywords': [
                    'Супервайзер отдела продаж',
                    'Директор по продажам и развитию',
                    'Директор по продажам',
                    'Директор по развитию',
                    'Менеджер по развитию',
                    'Руководитель отдела',
                    'Генеральный директор',
                    'Руководитель группы',
                    'Коммерческий директор',
                    'Ведущий менеджер по продажам',
                    'Руководитель направления',
                    'Руководитель департамента',
                    'Начальник отдела',
                    'Заместитель руководителя',
                    'Директор по продажам',
                    'Специалист по работе с клиентами',
                    'Директор по работе с клиентами',
                    'Account manager',
                    'Business development director',
                    'Business development manager',
                    'Аккаунт-менеджер',
                    'Аккаунт-директор',
                    'Региональный менеджер',
                ],
                'params': {
                    'specialization': ','.join([str(234)]),
                    'payment_from': 30000,
                    'age_from': 30,
                    'age_to': 50,
                    'period': '60',
                    # 'experience_to': 3*12,
                    'experience_from': 3*12,
                }
            },
            'Страховой агент': {
                'keywords': [
                    'Страховой агент',
                    'Руководитель отдела страхования',
                    'Специалист по страхованию',
                    'Страховой консультант',
                    'Страховой агент НПФ',
                    'Страховой представителль',
                    'Страховой брокер',
                ],
                'params': {
                    'payment_from': 25000,
                    'period': '60',
                    'age_from': 25,
                    'age_to': 60,
                }
            },
            'Рано на пенсию': {
                'keywords': [
                    'Учитель начальных классов',
                    'Педагог',
                    ' учитель',
                    ' стоматолог'
                    # 'летчик',
                    # 'шахтер',
                    # 'МЧС',
                    # 'военный',
                    'воспитатель',
                    'воспитатель детского сада',
                    'врач',
                    # 'геолог',
                    # 'гинеколог',
                    'доктор',
                    # 'железнодорожник',
                    # 'крановщик',
                    # 'криминалист',
                    # 'машинист',
                    'машинист крана',
                    'машинист локомотива',
                    'машинист поезда',
                    'медсестра',
                    # 'милиционер',
                    # 'моряк',
                    # 'нефтяник',
                    # 'педагог',
                    # 'пилот',
                    'пожарный',
                    'полицейский',
                    # 'прокурор',
                    # 'сварщик',
                    # 'следователь',
                    # 'спасатель',
                    # 'учитель',
                    'фармацевт',
                    # 'фельдшер',
                ],
                'params': {
                    'gender': 3,
                    'age_from': 37,
                    'payment_from': 40000,
                    'period': '60',
                }
            },
            'Топ руководители': {
                'keywords': [
                    'Директор филиала',
                    'Генеральный директор',
                    'Индивидуальный предприниматель',
                    'Заместитель генерального директора',
                    'Исполнительный директор ',
                    'Операционный директор',
                ],
                'params': {
                    'specialization': ','.join(map(str, [499, 33, 11, 284, 493, 492, 471, 482, 438])),
                    'age_from': 40,
                    'period': '60',
                }
            },
            # 'Сетевики MLM': {
            #     'keywords': [
            #         'Представитель компании',
            #         'Продавец-консультант',
            #         'Консультант',
            #     ],
            #     'params': {
            #         'gender': 3,
            #         'age_from': 25,
            #         'payment_from': 30000,
            #         'and_keywords': [
            #             'Avon',
            #             'Amway',
            #             'GRS',
            #             'Орифлейм',
            #             'Monavie',
            #             'Mageric ',
            #             'Маджерик',
            #             'Qnet',
            #             'QwertyPAY',
            #             'Santegra',
            #             'Sigcess',
            #             'Silkway',
            #             'Sisel',
            #             'SkinnyBodyCare',
            #             'Stemtech',
            #             'Tiens ',
            #             'Тяньши',
            #             'Tiande ',
            #             'Тианде',
            #             'Tupperware ',
            #             'Тапервер',
            #             'Vitaline ',
            #             'Виталайн',
            #             'Vivasan',
            #             'Вивасан',
            #             'Biosea',
            #             'Essens',
            #             'eCosway',
            #             'Fohow',
            #             'Gtime',
            #             'Gloryon',
            #             'Гербалайф',
            #             'Kyani ',
            #             'Каяни',
            #             'Lambre',
            #             'Ламбре',
            #             'Mirra',
            #             'Мирра',
            #
            #             # 'Neways',
            #             # 'Ньювейс',
            #             # 'Никкен',
            #             # 'TopLife',
            #             # 'Лавилайтс',
            #             # 'Litani',
            #             # 'Riway',
            #             # 'ЛиВест',
            #             # 'Winalite ',
            #             # 'Виналайт',
            #             # 'Xango',
            #             # 'Zepter ',
            #             # 'Цептер',
            #             # 'Аромашарм',
            #             # 'Биомедис',
            #             # 'Батель',
            #             # 'Витамакс',
            #             # 'Глорион',
            #
            #             # 'ДЭНАС',
            #             # 'ДЕТА-ЭЛИС',
            #             # 'Дайна',
            #             # 'Едоша',
            #             # 'Мейтан',
            #             # 'ННПЦТО',
            #             # 'НПЦРиЗ',
            #             # 'Омегавит',
            #             # 'Тенториум',
            #             # 'Фермион',
            #             # 'Эскалат',
            #             # 'Эковита',
            #             # 'Ялма',
            #             # 'Desheli',
            #             # 'Armelle',
            #             # 'JafraДжафра',
            #             # 'Ипар',
            #             # 'LuckLife',
            #             # 'Флоранж',
            #             # 'Deesse',
            #
            #         ]
            #     }
            # },
        }

        site = Site.objects.filter(title=CLIENT_SUPREJOB).first()

        for city in cities:
            for segment_name, segment_params in tasks.items():
                for keyword in segment_params.get('keywords'):
                    search_params = segment_params.get('params', {})
                    search_params.update({'town_id': city})
                    Task(
                        keyword=keyword,
                        segment=segment_name,
                        site=site,
                        limit=site.limit,
                        search_params=json.dumps(search_params),
                        status=Task.STATUS_IN_QUEUE
                    ).save()

    # @staticmethod
    # def add_task(site: Site, keyword: str, limit: int, search_params: dict):
    #     and_keywords = search_params.get('and_keywords', [])[:]
    #     for search_params_chunk in Command.batch(and_keywords):
    #         if len(search_params_chunk) > 0:
    #             search_params.update({'and_keywords': search_params_chunk})
    #
    # @staticmethod
    # def batch(iterable, size=100):
    #     l = len(iterable)
    #     for chunk in range(0, int(l / size) + 1):
    #         yield iterable[chunk*size:(chunk+1)*size]
