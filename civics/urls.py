# Import django apps
from django.conf.urls import url, include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
from django.views.defaults import page_not_found
# Import contrib apps
from registration.backends.default.views import RegistrationView
# Import custom apps
from apps.users.forms import RegistrationFormCaptcha
from apps.users.views import ActivationView
from apps.models.views import Resources

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^api/', include('apps.api.urls')),
    url(r'^jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('captcha/', include('captcha.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^$', TemplateView.as_view(template_name='pages/front.html'), name="front"),
    url(r'^', include('apps.models.urls')),

    # Static URLs
    url(r'^acerca$', TemplateView.as_view(template_name='pages/about.html'), name="about"),
    url(r'^recursos$', Resources.as_view(template_name='pages/resources.html'), name="resources"),
    url(r'^privacidad$', TemplateView.as_view(template_name='pages/privacy.html'), name="privacy"),

    # Registration URLs
    url(r'^activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),
    url(r'^registrate/$', RegistrationView.as_view(form_class=RegistrationFormCaptcha), name="registration_register"),
    url(r'^register/$', RedirectView.as_view(permanent=False, url='/registrate' ), name="registration_register_404"),
    url(r'^me-olvide-el-pass', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^confirma-pass/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    url(r'^pass-cambiado/$', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    url(r'^pass/ok/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'', include('registration.backends.default.urls')),
    url(r'^', include('apps.users.urls')),

    # Contact form
    url(r'^contacta/', include('contact_form.urls')),
)

if settings.DEBUG == True:
  urlpatterns += static( settings.STATIC_URL, document_root = settings.STATIC_ROOT )
  urlpatterns += static( settings.MEDIA_URL,  document_root = settings.MEDIA_ROOT )
