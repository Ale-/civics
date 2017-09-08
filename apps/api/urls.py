from django.conf.urls import url, include
from apps.models.models import Initiative
from . import views

urlpatterns = [
    url(r'^initiative$', views.initiative_service, name='get_initiative'),
    url(r'^initiatives$', views.initiatives_service, name='get_initiatives'),
    url(r'^initiatives_featured$', views.initiatives_featured_service, name='get_initiatives_featured'),
    url(r'^initiatives_performance$', views.initiatives_performancetest_service, name='test_initiatives'),
    url(r'^initiatives_xls$', views.initiatives_service_xls, name='get_initiatives_xls'),
    url(r'^event$', views.event_service, name='get_event'),
    url(r'^event_create$', views.create_event, name='create_event'),
    url(r'^events_fb_id$', views.events_by_fb_id_service, name='events_by_fb_id'),
    url(r'^events$', views.events_service, name='get_events'),
    url(r'^events_featured$', views.events_featured_service, name='get_events_featured'),
    url(r'^events_xls$', views.events_service_xls, name='get_events_xls'),
    url(r'^autocomplete$', views.autocomplete_service, name='autocomplete'),
    url(r'^cities_with_initiatives$', views.cities_with_initiatives, name='cities_with_initiatives'),
    url(r'^cities_with_events$', views.cities_with_events, name='cities_with_events'),
]
