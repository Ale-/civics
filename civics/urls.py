from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView
from apps.models.views import InitiativeCreate

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='pages/front.html'), name="front"),
    url(r'^', include('apps.models.urls', namespace='modelforms')),

    # Static URLs
    url(r'^acerca$', TemplateView.as_view(template_name='pages/about.html'), name="about"),

    # Registration URLs
    url(r'^registrate/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name="registration_register"),
    url(r'', include('registration.backends.default.urls')),
    url(r'^api/', include('apps.api.urls', namespace="api")),
    url(r'^user/', include('apps.users.urls', namespace="users")),
]
