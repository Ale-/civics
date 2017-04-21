from django.test import TestCase
from . import models
from djgeojson.fields import PointField

class CityTest(TestCase):

    """ Create a city """
    def create_city(self):
        return models.City.objects.create(name="Eutropia", country="VA", position ="POINT (0.0 0.0)" )

    """ Test city creation """
    def test_city_creation(self):
        city = self.create_city()
        self.assertTrue(isinstance(city, models.City))
        self.assertTrue(city.__str__, city.name)

class InitiativeTest(TestCase):

    """ Create a initiative """
    def create_initiative(self):
        city = CityTest.create_city(self)
        return models.Initiative.objects.create(
            name         = "Test initiative",
            description  = "Lorem ipsum",
            website      = "http://example.com",
            twitter      = "http://twitter.com",
            facebook     = "http://facebook.com",
            email        = "test@example.com",
            topic        = "OT",
            space        = "OT",
            agent        = "IM",
            city         = city,
            neighborhood = "Test neighborhood",
            position     = city.latlon,
        )

    """ Test city creation """
    def test_initiative_creation(self):
        initiative = self.create_initiative()
        self.assertTrue(isinstance(initiative, models.Initiative))
        self.assertTrue(initiative.__str__, initiative.name)
