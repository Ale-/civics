import random
from django.core.management.base import BaseCommand, CommandError
import csv, json, os.path
from apps.models.models import Initiative, ODS

"""
A manage.py command to migrate initiatives from a CSV file
"""

class Command(BaseCommand):


    """
    Add CSV file as an argument to the parser
    """
    def add_arguments(self, parser):
        parser.add_argument('csv_file')

    """
    Populates main ODS in Initiatives
    """
    def handle(self, *args, **options):
        if not os.path.isfile(options['csv_file']):
             raise CommandError('The specified file does not exist. Have you written it properly?')
        with open(options['csv_file'], 'r') as table:
            initiatives = csv.DictReader(table)
            for initiative in initiatives:
                try:
                    name = initiative['name']
                    i   = Initiative.objects.filter(name=name).first()
                    ods = ODS.objects.get(category=initiative['ods'])
                    i.main_ods = ods
                    i.save()
                    print(name, " saved")
                except Exception as e:
                    print(e, "[en ", name, "]")
