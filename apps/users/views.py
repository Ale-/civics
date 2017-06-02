from django.shortcuts import render
from django.views import View
from apps.models.models import City
from apps.models import categories
from registration.views import ActivationView as BaseActivationView
from registration.models import RegistrationProfile
from registration import signals
from django.contrib.sites.shortcuts import get_current_site

class Dashboard(View):

    def get(self, request):
        return render(request, 'users/dashboard.html', locals())


# Custom activation view that redirects user to Create Initiative form

class ActivationView(BaseActivationView):

    registration_profile = RegistrationProfile

    def activate(self, *args, **kwargs):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.

        """
        activation_key = kwargs.get('activation_key', '')
        site = get_current_site(self.request)
        activated_user = (self.registration_profile.objects
                          .activate_user(activation_key, site))
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=self.request)
        return activated_user

    def get_success_url(self, user):
        return ('modelforms:create_initiative', (), {})
