from django.conf.urls import url, include
from apps.models.models import Initiative
from . import views

urlpatterns = [
    url(r'^initiative$', views.initiative_service, name='get_initiative'),
    url(r'^initiatives$', views.initiatives_service, name='get_initiatives'),
    url(r'^initiatives_list$', views.initiatives_list_service, name='get_initiatives_list'),
    url(r'^initiatives_xls$', views.initiatives_service_xls, name='get_initiatives_xls'),
    url(r'^event$', views.event_service, name='get_event'),
    url(r'^events$', views.events_service, name='get_events'),
    url(r'^events_list$', views.events_list_service, name='get_events_list'),
    url(r'^events_xls$', views.events_service_xls, name='get_events_xls'),
    url(r'^cities$', views.cities_service, name='get_cities'),
    url(r'^countries$', views.countries_service, name='get_countries'),
    url(r'^autocomplete$', views.autocomplete_service, name='autocomplete'),
]
