from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='pages/front.html'), name="front"),
    url(r'^', include('apps.models.urls', namespace='modelforms')),
]
