# django
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
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
        google_client_id = settings.GOOGLE_CLIENT_ID
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

class UserDelete(DeleteView):

    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:thanks')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Tu cuenta ha sido cancelada'))
        pk = request.user.pk
        mail = User.objects.get(pk=pk).email
        send_mail(
            _('Tu cuenta en civics.cc ha sido cancelada'),
            _('Te confirmamos que la cuenta '
              'asociada a este correo en civics.cc ha sido borrada con éxito. '
              'Este es un correo automático. No lo respondas.'
             ),
            'no-reply@civics.cc',
            [mail]
        )
        return super(UserDelete, self).delete(request, *args, **kwargs)

    def get_object(self):
        pk = self.request.user.pk
        return User.objects.get(pk=pk)
