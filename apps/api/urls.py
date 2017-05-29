from django.conf.urls import url, include
from apps.models.models import Initiative
from . import views

urlpatterns = [
    url(r'^initiatives$', views.initiatives_service, name='get_initiatives'),
    url(r'^events$', views.events_service, name='get_events'),
    url(r'^initiatives_xls$', views.initiatives_service_xls, name='get_initiatives_xls'),
    url(r'^cities$', views.cities_service, name='get_cities'),
]
