from django.core.management.base import BaseCommand, CommandError
from apps.models.models import Initiative

# TODO: tests!!!

"""
A manage.py command to migrate cities from a CSV file
"""

class Command(BaseCommand):
    help = "Delete all Initiative models from database."

    """
    Deletes all Initiative objects
    """
    def handle(self, *args, **options):
        Initiative.objects.all().delete()
