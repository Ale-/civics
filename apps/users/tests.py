# Import generic python packages
from urllib.parse import urlencode
# Import from django apps
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
# Import from contrib apps
from model_mommy import mommy


class UserTest(TestCase):
    """ User related tests """

    def test_views(self):
        """ Test modelform views related to City model """

        c = Client()
        # Test that anonymous users cannot access to the dashboard
        url = reverse('users:dashboard')
        response = c.get(url, follow=True)
        self.assertRedirects(response, reverse('auth_login') + '?' + urlencode({'next' : url}))
        # Test that anonymous users cannot access to the staff dashboard
        url = reverse('users:dashboard_staff')
        response = c.get(url, follow=True)
        self.assertRedirects(response, reverse('admin:login') + '?next=' + url )
        # Test that registered users can access the dashboard
        self.test_user = mommy.make('User',  username='test', password = 'paxxword', is_active = True)
        c.login(username='test', password='paxxword')
        response = c.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        # Test that registered users cannot access to the staff dashboard
        url = reverse('users:dashboard_staff')
        response = c.get(url, follow=True)
        self.assertRedirects(response, reverse('admin:login') + '?next=' + url )
