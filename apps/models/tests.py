# Import generic python packages
from datetime import date
from urllib.parse import urlencode
# Import from django apps
from django.test import TestCase
from django.test import Client
from djgeojson.fields import PointField
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
# Import from contrib apps
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key
# Import from custom apps
from . import models
from django.contrib.auth.models import User


class CityTest(TestCase):
    """ Test City model """

    def test_views(self):
        """ Test modelform views related to City model """
        c = Client()
        # Check that views redirect to login page when user is anonymous
        # Create
        url = reverse('modelforms:create_city_popup')
        response = c.get(url, follow=True)
        self.assertRedirects(response, reverse('auth_login') + '?' + urlencode({'next' : url}))
        # Check views for registered users
        self.test_user = mommy.make('User',  username='test', password = 'paxxword', is_active = True)
        c.login(username='test', password='paxxword')
        response = c.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_node_creation(self):
        """ Test instance creation """
        node = mommy.make("models.City", position ="POINT (0.0 0.0)")
        self.assertTrue(isinstance(node, models.City))
        # Check string representation
        self.assertEqual(node.__str__(), node.name)


class InitiativeTest(TestCase):
    """ Test Initiative model """

    def test_node_creation(self):
        """ Test instance creation """
        node = mommy.make("models.Initiative", position ="POINT (0.0 0.0)")
        self.assertTrue(isinstance(node, models.Initiative))
        # Check string representation
        self.assertEqual(node.__str__(), node.name)
        # Check fields
        self.assertEqual(node.slug, slugify(node.name))
        self.assertEqual(node.creation_date.day, timezone.now().day)

    def test_views(self):
        """ Test modelform views related to Initiative model """
        c = Client()
        # Check that views redirect to login page when user is anonymous
        # Create
        url = reverse('modelforms:create_initiative')
        response = c.get(url, follow=True)
        self.assertRedirects(response, reverse('auth_login') + '?' + urlencode({'next' : url}))
        # Edit
        url = reverse('modelforms:edit_initiative', kwargs={'pk':1} )
        response = c.get(url, follow=True)
        self.assertRedirects(response, reverse('auth_login') + '?' + urlencode({'next' : url}))
        # Delete
        url = reverse('modelforms:delete_initiative', kwargs={'pk':1} )
        response = c.get(url, follow=True)
        self.assertRedirects(response, reverse('auth_login') + '?' + urlencode({'next' : url}))
        # Check views for registered users
        self.user = User.objects.create_user(username='test', email='test@test.test', password='paxxword')
        c.login(username='test', password='paxxword')
        initiative = mommy.make("models.Initiative", name="Test", position ="POINT (0.0 0.0)", pk=1)
        response = c.get(reverse('modelforms:create_initiative'), follow=True)
        self.assertEqual(response.status_code, 200)
        # Test unauthorized users cannot update data
        response = c.get(reverse('modelforms:edit_initiative', kwargs={'pk':1}), follow=True)
        self.assertEqual(response.status_code, 403)
        response = c.get(reverse('modelforms:delete_initiative', kwargs={'pk':1}), follow=True)
        self.assertEqual(response.status_code, 403)
        # Test authorized staff users can update data
        self.user.is_staff = True
        self.user.save()
        response = c.get(reverse('modelforms:edit_initiative', kwargs={'pk':1}), follow=True)
        self.assertEqual(response.status_code, 200)
        response = c.get(reverse('modelforms:delete_initiative', kwargs={'pk':1}), follow=True)
        self.assertEqual(response.status_code, 200)


class EventTest(TestCase):
    """ Test Event model """

    def test_node_creation(self):
        """ Test instance creation """
        node = mommy.make("models.Event", position ="POINT (0.0 0.0)")
        self.assertTrue(isinstance(node, models.Event))
        # Check string representation
        self.assertEqual(node.__str__(), node.title)
        # Check fields
        self.assertEqual(node.slug, slugify(node.title))
        self.assertEqual(node.creation_date.day, timezone.now().day)

    def test_views(self):
        """ Test modelform views related to Initiative model """
        c = Client()
        # Check that views redirect to login page when user is anonymous
        # Create
        url = reverse('modelforms:create_event')
        response = c.get(url, follow=True)
        self.assertRedirects(response, reverse('auth_login') + '?' + urlencode({'next' : url}))
        # Edit
        url = reverse('modelforms:edit_event', kwargs={'pk':1} )
        response = c.get(url, follow=True)
        self.assertRedirects(response, reverse('auth_login') + '?' + urlencode({'next' : url}))
        # Delete
        url = reverse('modelforms:delete_event', kwargs={'pk':1} )
        response = c.get(url, follow=True)
        self.assertRedirects(response, reverse('auth_login') + '?' + urlencode({'next' : url}))
        # Check views for registered users
        self.user = User.objects.create_user(username='test', email='test@test.test', password='paxxword')
        c.login(username='test', password='paxxword')
        event = mommy.make("models.Event", title="Test", position ="POINT (0.0 0.0)", pk=1)
        response = c.get(reverse('modelforms:create_event'), follow=True)
        self.assertEqual(response.status_code, 200)
        # Test unauthorized users cannot update data
        response = c.get(reverse('modelforms:edit_event', kwargs={'pk':1}), follow=True)
        self.assertEqual(response.status_code, 403)
        response = c.get(reverse('modelforms:delete_event', kwargs={'pk':1}), follow=True)
        self.assertEqual(response.status_code, 403)
        # Test authorized staff users can update data
        self.user.is_staff = True
        self.user.save()
        response = c.get(reverse('modelforms:edit_event', kwargs={'pk':1}), follow=True)
        self.assertEqual(response.status_code, 200)
        response = c.get(reverse('modelforms:delete_event', kwargs={'pk':1}), follow=True)
        self.assertEqual(response.status_code, 200)
