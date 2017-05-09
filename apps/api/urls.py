from django.conf.urls import url, include
from apps.models.models import Initiative
from . import views

urlpatterns = [
    url(r'^initiatives$',
        views.initiatives_service,
        name='get_initiatives'),
]
