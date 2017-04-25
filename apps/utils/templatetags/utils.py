from django import template
from django.utils.translation import ugettext_lazy as _
from civics.settings import STATIC_URL, PROJECT_STATIC_FOLDER

register = template.Library()

@register.simple_tag
def css(file):
    return  STATIC_URL + PROJECT_STATIC_FOLDER + '/css/' + file

@register.simple_tag
def js(file):
    return  STATIC_URL + PROJECT_STATIC_FOLDER + '/js/' + file

@register.simple_tag
def img(file):
    return  STATIC_URL + PROJECT_STATIC_FOLDER + '/img/' + file
