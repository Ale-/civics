from django import template
from django.utils.translation import ugettext_lazy as _
from civics.settings import STATIC_URL, PROJECT_STATIC_FOLDER
from django.utils.safestring import mark_safe

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
