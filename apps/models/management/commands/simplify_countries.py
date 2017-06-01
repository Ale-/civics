from django.core.management.base import BaseCommand, CommandError
import json, os.path
import re
from termcolor import colored

# TODO: tests!!!

"""
A manage.py command to migrate cities from a CSV file
"""

class Command(BaseCommand):
    help = "Simplify geoJSON data to reduce its weight."

    """
    Add CSV file as an argument to the parser
    """
    def add_arguments(self, parser):
        parser.add_argument('geojson_file')
        parser.add_argument('decimals')

    """
    Imports City models from a given CSV file
    """
    def handle(self, *args, **options):
        source_file = options['geojson_file']
        decimals    = options['decimals']

        if not os.path.isfile( source_file ):
            raise CommandError('The specified file does not exist. Have you written it properly?')

        with open(source_file, 'r') as geojson:
            countries_data =  geojson.read()
            # Reduce accuracy
            print("\nReducing accuracy of floating point numbers to " + decimals + " digits")
            countries_simplified_data = re.sub('([-]?\d{1,3}\.\d{' + decimals + '})\d*', '\g<1>', countries_data)
            # Remove unnecesary information
            print("Removing unnecesary information")
            countries = json.loads(countries_simplified_data)['features']
            for country in countries:
                country.pop('properties')

        source_folder   = os.path.dirname(geojson.name)
        source_basename = os.path.splitext(os.path.basename(geojson.name))[0]
        print(source_basename)
        target_path     = source_folder + "/" + source_basename + '--simplified.json'
        source_size     = os.path.getsize(geojson.name)
        print("Saving " + target_path)
        with open(target_path, 'w') as target_file:
            target_file.write( json.dumps(countries) )
            target_size = os.path.getsize(target_file.name)
            print(colored("Done! Reduced " + '{0:.2f}'.format(100 - target_size/source_size*100) + " % of source size. \n", "yellow"))
