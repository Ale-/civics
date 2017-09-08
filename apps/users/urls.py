from django.conf.urls import url, include
from apps.models.models import Initiative
from . import views

urlpatterns = [
    url(r'^mi-perfil$', views.Dashboard.as_view(), name='dashboard'),
]
