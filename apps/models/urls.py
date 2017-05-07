from django.conf.urls import url
from . import views
from apps.utils.views import PopupFormView
from .forms import CityForm

urlpatterns = [
    url(r'^crea/ciudad$', PopupFormView.as_view(form_class=CityForm, template_name="forms/city-popup-form.html"), name="create_city_popup"),
    url(r'^crea/ciudad$', views.CityCreate.as_view(), name="create_city"),
    url(r'^edita/ciudad/(?P<pk>.+)$', views.CityEdit.as_view(), name="edit_city"),
    url(r'^borra/ciudad(?P<pk>.+)$', views.CityDelete.as_view(), name="delete_city"),

    url(r'^crea/iniciativa$', views.InitiativeCreate.as_view(), name="create_initiative"),
    url(r'^edita/iniciativa/(?P<slug>.+)$', views.InitiativeEdit.as_view(), name="edit_initiative"),
    url(r'^borra/iniciativa/(?P<slug>.+)$', views.InitiativeDelete.as_view(), name="delete_initiative"),

    url(r'^crea/evento$', views.EventCreate.as_view(), name="create_event"),
    url(r'^edita/evento/(?P<slug>.+)$', views.EventEdit.as_view(), name="edit_event"),
    url(r'^borra/evento(?P<slug>.+)$', views.EventDelete.as_view(), name="delete_event"),
]
