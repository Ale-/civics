import random
from django.core.management.base import BaseCommand, CommandError
import csv, json, os.path
from apps.models.models import Initiative, ODS

"""
A manage.py command to migrate initiatives from a CSV file
"""

class Command(BaseCommand):

    """
    Populates main ODS in Initiatives
    """
    def handle(self, *args, **options):
        ods         = ODS.objects.all()
        ods_array   = [ o for o in ods ]
        initiatives = Initiative.objects.all()
        for i in initiatives:
            i.main_ods = random.choice(ods_array)
            i.save()
