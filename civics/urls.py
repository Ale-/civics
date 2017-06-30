from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView
from apps.users.views import ActivationView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='pages/front.html'), name="front"),
    url(r'^', include('apps.models.urls', namespace='modelforms')),

    # Static URLs
    url(r'^acerca$', TemplateView.as_view(template_name='pages/about.html'), name="about"),

    # Registration URLs
    url(r'^activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),
    url(r'^registrate/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name="registration_register"),
    url(r'^me-olvide-el-pass', auth_views.password_reset, name='password_reset'),
    url(r'^confirma-pass/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name="password_reset_confirm"),
    url(r'^pass-cambiado/$', auth_views.password_reset_complete, name="password_reset_complete"),
    url(r'^pass/ok/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'', include('registration.backends.default.urls')),
    url(r'^api/', include('apps.api.urls', namespace="api")),
    url(r'^', include('apps.users.urls', namespace="users")),

    # Contact form
    url(r'^contacta/', include('contact_form.urls')),
]

if settings.DEBUG == True:
  urlpatterns += static( settings.STATIC_URL, document_root = settings.STATIC_ROOT )
  urlpatterns += static( settings.MEDIA_URL,  document_root = settings.MEDIA_ROOT )
