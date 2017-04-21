from django.core.management.base import BaseCommand, CommandError
from models.models import City


# TODO: tests!!!

"""
A manage.py command to migrate cities from a CSV file
"""

class Command(BaseCommand):
    help = "Delete all City models from database."

    """
    Deletes all City objects
    """
    def handle(self, *args, **options):
        City.objects.all().delete()
