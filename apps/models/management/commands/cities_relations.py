from django.core.management.base import BaseCommand, CommandError
from apps.models.models import City, Initiative, Event


# TODO: tests!!!

"""
A manage.py command to create relations between Cities and other models
"""

class Command(BaseCommand):
    help = "Populate City relations fields."

    """
    Deletes all City objects
    """
    def handle(self, *args, **options):
        cities = City.objects.all()
        for city in cities:
            related_initiatives = Initiative.objects.filter(city=city).count()
            if related_initiatives > 0:
                city.initiative_related = True
            related_events = Event.objects.filter(city=city).count()
            if related_events > 0:
                city.event_related = True
            city.save()
