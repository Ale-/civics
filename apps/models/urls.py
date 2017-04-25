from django.conf.urls import url
from . import views


urlpatterns = [

    #
    #  City modelforms
    #
    url(r'^crea/ciudad$', views.CityCreate.as_view(), name="create_city"),
    # Edit project form
    url(r'^edita/ciudad/(?P<pk>.+)$', views.CityEdit.as_view(), name="edit_city"),
    # Remove project form
    url(r'^borra/ciudad(?P<pk>.+)$', views.CityDelete.as_view(), name="delete_city"),

    #
    #  Initiative modelforms
    #
    url(r'^crea/iniciativa$', views.InitiativeCreate.as_view(), name="create_initiative"),
    # Edit project form
    url(r'^edita/iniciativa/(?P<slug>.+)$', views.InitiativeEdit.as_view(), name="edit_initiative"),
    # Remove project form
    url(r'^borra/iniciativa/(?P<slug>.+)$', views.InitiativeDelete.as_view(), name="delete_initiative"),

    #
    #  Event modelforms
    #
    url(r'^crea/evento$', views.EventCreate.as_view(), name="create_event"),
    # Edit project form
    url(r'^edita/evento/(?P<slug>.+)$', views.EventEdit.as_view(), name="edit_event"),
    # Remove project form
    url(r'^borra/evento(?P<slug>.+)$', views.EventDelete.as_view(), name="delete_event"),


]
