from django.test import TestCase
from . import models
from djgeojson.fields import PointField

class cityTest(TestCase):

    """ Create a city """
    def create_city(self):
        return models.City.objects.create(name="Eutropia", country="VA", latlon ="POINT (0.0 0.0)" )

    """ Test city creation """
    def test_city_creation(self):
        city = self.create_city()
        self.assertTrue(isinstance(city, models.City))
        self.assertTrue(city.__str__, city.name)
