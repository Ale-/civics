# django
from django.conf.urls import url
from django.views.generic import TemplateView
# project
from apps.utils.views import PopupFormView
from . import views
from .forms import CityForm

urlpatterns = [
    url(r'^crea/ciudad$', PopupFormView.as_view(form_class=CityForm, template_name="forms/city-popup-form.html"), name="create_city_popup"),

    url(r'^crea/iniciativa$', views.InitiativeCreate.as_view(), name="create_initiative"),
    url(r'^edita/iniciativa/(?P<pk>.+)$', views.InitiativeEdit.as_view(), name="edit_initiative"),
    url(r'^relaciona/iniciativa/(?P<pk>.+)$', views.InitiativeRelate.as_view(), name="relate_initiative"),
    url(r'^borra/iniciativa/(?P<pk>.+)$', views.InitiativeDelete.as_view(), name="delete_initiative"),
    url(r'^bienvenido$', TemplateView.as_view(template_name='pages/initiative-success.html'), name="welcome_initiative"),

    url(r'^crea/evento$', views.EventCreate.as_view(), name="create_event"),
    url(r'^edita/evento/(?P<pk>.+)$', views.EventEdit.as_view(), name="edit_event"),
    url(r'^borra/evento/(?P<pk>.+)$', views.EventDelete.as_view(), name="delete_event"),
]
