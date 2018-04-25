import csv
import logging

from django.core.management import BaseCommand
from django.utils.timezone import now

from app.settings import BASE_DIR
from scrapper.models import Task, Profile

log = logging.getLogger('console')


class Command(BaseCommand):
    help = "city / segment matrix"

    def handle(self, *args, **options):
        profiles = Profile.objects.all()

        # 2 dim dictionary from all records
        m = {}
        for profile in profiles:
            if profile.segment in m and profile.city in m[profile.segment]:
                m[profile.segment][profile.city] += 1
            else:
                if profile.segment not in m:
                    m[profile.segment] = dict()
                m[profile.segment].update({profile.city: 1})
        self.write_csv(m,  '{}/files/csv/by_segment_{}.csv'.format(BASE_DIR, now()))

    def write_csv(self, d: dict, file: str):
        cities = set()
        for city_dict in d.values():
            for city in city_dict.keys():
                cities.add(city)
        cities = list(cities)

        with open(file, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([''] + cities)

            for seg_name, seg in d.items():
                counts = []
                for city in cities:
                    counts.append(seg.get(city, 0))
                writer.writerow([seg_name] + counts)
