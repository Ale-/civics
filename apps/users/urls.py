# django
from django.conf.urls import url, include
from django.views.generic import TemplateView
# project
from apps.models.models import Initiative
from . import views

urlpatterns = [
    url(r'^mi-perfil$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^gracias$',   TemplateView.as_view(template_name='pages/goodbay.html'), name='thanks'),
    url(r'^sign-out/(?P<slug>.+)$', views.UserDelete.as_view(), name='signout')
]
