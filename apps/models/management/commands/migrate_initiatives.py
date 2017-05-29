from django.core.management.base import BaseCommand, CommandError
import csv, json, os.path
from apps.models.models import Initiative, City
from django.utils.text import slugify

# TODO: tests!!!

"""
A manage.py command to migrate initiatives from a CSV file
"""

class Command(BaseCommand):
    help = "Instantiate Initiatives models from a CSV file. Following columns are needed: \
            'Name', 'Code' (contrycode in ISO ISO 3166-2), 'Longitude' and 'Latitude' \
            The only argument is a valid path to the CSV file."

    """
    Add CSV file as an argument to the parser
    """
    def add_arguments(self, parser):
        parser.add_argument('csv_file')

    """
    Imports Initiative models from a given CSV file
    """
    def handle(self, *args, **options):
        if not os.path.isfile(options['csv_file']):
             raise CommandError('The specified file does not exist. Have you written it properly?')
        with open(options['csv_file'], 'r') as initiatives_file:
            initiatives = csv.DictReader(initiatives_file)
            initiatives_objects = map(
                lambda i: Initiative(
                    name        = i['Name'],
                    slug        = slugify(i['Name']),
                    topic       = i['Topic'],
                    space       = i['Space'],
                    agent       = i['Agent'],
                    description = i['Description'],
                    website     = i['Website'],
                    email       = i['Email'],
                    twitter     = i['Twitter'],
                    facebook    = i['Facebook'],
                    city        = City.objects.filter(name=i['City']).first(),
                    address     = i['Address'],
                    district    = i['District'],
                    position    = json.loads('{ "type": "Point", "coordinates": [' + i['Longitude'] + ',' + i['Latitude'] +'] }')
                ),
                initiatives
            )
            Initiative.objects.bulk_create(initiatives_objects)
