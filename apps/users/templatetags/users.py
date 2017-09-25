# django
from django import template
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
# project
from apps.models.categories import ACTIVITIES as activities
from apps.models.models import Initiative
register = template.Library()

@register.inclusion_tag('events_import.js.html')
def events_import_js(user_initiatives=None):
    """ Tag to embed scripts needed to import events from social networks """
    initiatives = user_initiatives
    event_categories = activities
    facebook_id = settings.FACEBOOK_APP_ID,
    return locals()

@register.inclusion_tag('dashboard_leaflet.js.html')
def dashboard_leaflet_js(user_initiatives=None):
    """ Tag to embed scripts needed to display a map with user's initiatives in dashboard """
    initiatives = user_initiatives
    return locals()
