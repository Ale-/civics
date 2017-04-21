from django.core.management.base import BaseCommand, CommandError
import csv, json, os.path
from models.models import City


# TODO: tests!!!

"""
A manage.py command to migrate cities from a CSV file
"""

class Command(BaseCommand):
    help = "Instantiate City models from a CSV file. Following columns are needed: \
            'Name', 'Code' (contrycode in ISO ISO 3166-2), 'Longitude' and 'Latitude' \
            The only argument is a valid path to the CSV file."

    """
    Add CSV file as an argument to the parser
    """
    def add_arguments(self, parser):
        parser.add_argument('csv_file')

    """
    Imports City models from a given CSV file
    """
    def handle(self, *args, **options):
        if not os.path.isfile(options['csv_file']):
             raise CommandError('The specified file does not exist. Have you written it properly?')
        with open(options['csv_file'], 'r') as cities_file:
            cities = csv.DictReader(cities_file)
            city_objects = map(
                lambda i: City(
                    name     = i['Name'],
                    city     = i['City'],
                    country  = i['Code'],
                    position = json.loads('{ "type": "Point", "coordinates": [' + i['Longitude'] + ',' + i['Latitude'] +'] }')
                ),
                cities
            )
            City.objects.bulk_create(city_objects)
