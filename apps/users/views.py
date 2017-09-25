# django
from django.shortcuts import render
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# contrib
from registration.views import ActivationView as BaseActivationView
from registration.models import RegistrationProfile
from registration import signals
# project
from apps.models.models import City, Initiative, Event
from apps.models import categories
from django.conf import settings


class Dashboard(LoginRequiredMixin, View):
    """
    Get user profile

    """

    def get(self, request):
        facebook_id = settings.FACEBOOK_APP_ID
        initiatives = Initiative.objects.filter(user=request.user).order_by('name')
        if initiatives:
            events      = Event.objects.filter(initiative__in=initiatives).all()
            return render(request, 'users/dashboard.html', locals())

        return HttpResponseRedirect( reverse('modelforms:create_initiative') )


class ActivationView(BaseActivationView):
    """
    Custom activation view that redirects user to Create Initiative form

    """

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
