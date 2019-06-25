import os.path
from django import template
from django.utils.translation import ugettext_lazy as _
from civics.settings import STATIC_URL, PROJECT_STATIC_FOLDER
from django.utils.safestring import mark_safe
from django.conf import settings
from apps.models.categories import RESOURCES

register = template.Library()

@register.simple_tag
def css(file):
    return  STATIC_URL + PROJECT_STATIC_FOLDER + '/css/' + file

@register.simple_tag
def js(file):
    return  STATIC_URL + PROJECT_STATIC_FOLDER + '/js/' + file

@register.simple_tag
def angular(file):
    return  mark_safe("<script type='text/javascript' src='" +STATIC_URL + PROJECT_STATIC_FOLDER + "/angular/" + file + "'></script>")

@register.simple_tag
def img(file):
    return  STATIC_URL + PROJECT_STATIC_FOLDER + '/img/' + file

@register.inclusion_tag('fake-breadcrumb.html')
def fake_breadcrumb(text="Volver a la página anterior"):
    return { 'text' : text }

@register.inclusion_tag('limited-choices-select.html')
def limited_choices_select(choices=None, select_name=None, select_class=None, all=False, multiple=False):
    options = [{ 'name' : option[1], 'id' : option[0] } for option in choices ]
    return  { 'options' : options, 'select_name' : select_name, 'select_class' : select_class, 'all' : all, 'multiple' : multiple}

@register.filter
def get_range(max):
    return range(max)

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter(name='remove_i18n_prefix')
def remove_i18n_prefix(value):
    if value.startswith('/en') or value.startswith('/es'):
        value = value[3::]
    return value

@register.filter(name='check_file')
def check_file(value):
    return value and os.path.isfile(settings.MEDIA_ROOT + "/" + value.name)

@register.assignment_tag
def FAQ():
    return [
        'what', 'where', 'for',
        'community', 'who', 'categories',
        'data', 'maintenance',
        'support', 'impact'
    ]

@register.simple_tag
def resource(value):
    resources = dict(RESOURCES)
    return resources[value]

@register.filter
def resource_name(obj, lang):
    return obj.get_name(lang)

@register.filter
def resource_summary(obj, lang):
    return obj.get_summary(lang)
