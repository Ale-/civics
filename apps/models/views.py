from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from apps.utils.views import GenericCreate, GenericUpdate, GenericDelete
from . import forms, models
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from .models import Initiative
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

# Model related views

modelform_generic_template = 'pages/modelform.html'
modelform_delete_template = 'pages/modelform--delete.html'

#
#  Initiative
#

class InitiativeCreate(GenericCreate):
  """Generic view to create Initiative objects."""

  model            = models.Initiative
  form_class       = forms.InitiativeForm
  form__html_class = 'initiative'
  template_name    = modelform_generic_template
  title            = _('Crea una iniciativa')

  def get_success_url(self):
      if self.request.user.is_staff:
          return reverse_lazy('dashboard')
      else:
          return reverse_lazy('modelforms:welcome_initiative')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(InitiativeCreate, self).form_valid(form)

  def get_context_data(self, **kwargs):
    """Pass context data to generic view."""
    context = super(InitiativeCreate, self).get_context_data(**kwargs)
    context['form__html_class'] = self.form__html_class
    context['submit_text'] = _('Crea la iniciativa')
    return context


class InitiativeEdit(GenericUpdate):
  """Generic view to edit Initiative objects."""
  model            = models.Initiative
  form_class       = forms.InitiativeForm
  form__html_class = 'initiative'
  template_name    = modelform_generic_template
  title            = _('Edita la información de la iniciativa ')
  success_url      = reverse_lazy('users:dashboard')

  def get_success_url(self):
    if Initiative.objects.filter(user = self.request.user).first():
        return reverse_lazy('users:dashboard')
    return ('/#!/iniciativas')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(InitiativeEdit, self).form_valid(form)

  def get_context_data(self, **kwargs):
    """Pass context data to generic view."""
    context                     = super(InitiativeEdit, self).get_context_data(**kwargs)
    pk                          = self.kwargs['pk']
    initiative                  = get_object_or_404(models.Initiative, pk=pk)
    context['title']            = self.title + (' ') + initiative.name
    context['form__html_class'] = self.form__html_class
    context['submit_text'] = _('Edita esta iniciativa')
    return context

class InitiativeDelete(GenericDelete):
  """Generic view to delete Initiative objects."""
  model            = models.Initiative
  form_class       = forms.InitiativeForm
  form__html_class = 'initiative'
  template_name    = modelform_delete_template
  title            = _('Borra la iniciativa ')
  success_url      = reverse_lazy('front')

  def get_context_data(self, **kwargs):
    """Pass context data to generic view."""
    context          = super(InitiativeDelete, self).get_context_data(**kwargs)
    pk               = self.kwargs['pk']
    initiative       = get_object_or_404(models.Initiative, pk=pk)
    context['title'] = self.title + (' ') + initiative.name
    context['form__html_class'] = self.form__html_class
    context['submit_text'] = _('¿Estás seguro de que quieres borrar esta iniciativa?')
    return context


#
#  Event
#

class EventCreate(GenericCreate):
  """Generic view to create Event objects."""

  model            = models.Event
  form_class       = forms.EventForm
  form__html_class = 'event'
  template_name    = modelform_generic_template
  title            = _('Crea un evento ')
  success_url      = reverse_lazy('users:dashboard')
  dependencies     = ['leaflet']

  def form_valid(self, form):
    user_initiative = Initiative.objects.filter(user=self.request.user).first()
    form.instance.initiative = user_initiative
    return super(EventCreate, self).form_valid(form)

  def get_context_data(self, **kwargs):
    """Pass context data to generic view."""
    context                     = super(EventCreate, self).get_context_data(**kwargs)
    context['form__html_class'] = self.form__html_class
    context['submit_text'] = _('Publica este evento')
    return context

  def get_initial(self):
    super(EventCreate, self).get_initial()
    user = self.request.user
    initiative = Initiative.objects.filter(user=user).first()
    return {
        "initiative"     : initiative
    }

class EventEdit(GenericUpdate):
  """Generic view to edit Event objects."""
  model = models.Event
  form_class = forms.EventForm
  template_name = modelform_generic_template
  form__html_class = 'event'
  title = _('Edita la información del evento ')
  dependencies     = ['leaflet']

  def form_valid(self, form):
    user_initiative = Initiative.objects.filter(user=self.request.user).first()
    form.instance.initiative = user_initiative
    return super(EventEdit, self).form_valid(form)

  def get_success_url(self):
    if Initiative.objects.filter(user = self.request.user).first():
        return reverse_lazy('users:dashboard')
    return ('/#!/eventos')

  def get_context_data(self, **kwargs):
    """Pass context data to generic view."""
    context                     = super(EventEdit, self).get_context_data(**kwargs)
    pk                          = self.kwargs['pk']
    event                       = get_object_or_404(models.Event, pk=pk)
    context['title']            = self.title + (' ') + event.title
    context['form__html_class'] = self.form__html_class
    context['submit_text'] = _('Edita este evento')
    return context

class EventDelete(GenericDelete):
  """Generic view to delete Event objects."""

  model            = models.Event
  title            = _('Borra el evento ')
  form__html_class = 'event'
  success_url      = reverse_lazy('front')
  template_name    = modelform_generic_template

  def get_context_data(self, **kwargs):
    """Pass context data to generic view."""
    context          = super(EventDelete, self).get_context_data(**kwargs)
    pk               = self.kwargs['pk']
    event            = get_object_or_404(models.Event, pk=pk)
    context['title'] = self.title + (' ') + event.title
    context['form__html_class'] = self.form__html_class
    return context
