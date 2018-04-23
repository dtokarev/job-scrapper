import json
import logging

from django.core.management import BaseCommand

from scrapper.models import Task, Site
from scrapper.service.client.client_api import SuperjobApiClient, CLIENT_SUPREJOB

log = logging.getLogger('console')


class Command(BaseCommand):
    help = "add new task to queue"

    def handle(self, *args, **options):
        cities = [33]
        # cities = [89, 42, 33, 130, 12, 13, 17, 119, 5, 173]

        tasks = segments = {
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
                    # 'Продавец-консультант',
                    # 'Консультант',
                ],
                'params': {
                    'gender': 3,
                    'age_from': 25,
                    'and_keywords': [
                        # 'Орифлэйм косметикс',
                        # 'Эйвон Бьюти Продак Компани',
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
