import csv
import os

from django.core.management.base import BaseCommand
from foodgram_project.settings import BASE_DIR
from ingredients.models import Ingredient, MeasurementUnit


class Command(BaseCommand):
    help = 'Копирование данных из csv'
    shift_path = os.path.join(BASE_DIR, 'start_data')

    def handle(self, *args, **kwargs):
        filename = os.path.join(self.shift_path, 'ingredients.csv')
        with open(filename, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in csv_reader:
                unit_data = row[1].strip().lower()
                ingrid_data = row[0].strip().lower()
                unit, _ = MeasurementUnit.objects.get_or_create(
                    name=unit_data
                )
                Ingredient.objects.create(
                    name=ingrid_data, measurement_unit=unit
                )
