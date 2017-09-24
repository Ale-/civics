# django
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
# project
from apps.utils.views import GenericCreate, GenericUpdate, GenericDelete
from . import forms, models
from .models import Initiative

# Model related templates

modelform_generic_template = 'pages/modelform.html'
modelform_delete_template  = 'pages/modelform--delete.html'

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
          return reverse_lazy('users:dashboard')
      else:
          return reverse_lazy('modelforms:welcome_initiative')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(InitiativeCreate, self).form_valid(form)

  def get_context_data(self, **kwargs):
    """Pass context data to generic view."""
    context = super(InitiativeCreate, self).get_context_data(**kwargs)
    context['form__html_class'] = self.form__html_class
    context['form__action_class'] = 'form-create'
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
    return reverse_lazy('users:dashboard')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(InitiativeEdit, self).form_valid(form)

  def get_context_data(self, **kwargs):
    """Pass context data to generic view."""
    context                       = super(InitiativeEdit, self).get_context_data(**kwargs)
    pk                            = self.kwargs['pk']
    initiative                    = get_object_or_404(models.Initiative, pk=pk)
    context['title']              = self.title + (' ') + initiative.name
    context['form__html_class']   = self.form__html_class
    context['form__action_class'] = 'form-edit'
    context['object_id']          = pk
    context['submit_text'] = _('Guarda los cambios')
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
    context['cancel_text'] = _('No, no estoy seguro.')
    return context

  def get_success_url(self):
    return reverse_lazy('users:dashboard')

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
    context['form__action_class'] = 'form-create'
    context['submit_text'] = _('Publica este evento')
    return context

  def get_initial(self):
    super(EventCreate, self).get_initial()
    return {
        "user" : self.request.user
    }

class EventEdit(GenericUpdate):
  """Generic view to edit Event objects."""
  model = models.Event
  form_class = forms.EventForm
  template_name = modelform_generic_template
  form__html_class = 'event'
  title = _('Edita el evento ')
  dependencies     = ['leaflet']

  def form_valid(self, form):
    if not self.request.user.is_staff:
      user_initiative = Initiative.objects.filter(user=self.request.user).first()
      form.instance.initiative = user_initiative
    return super(EventEdit, self).form_valid(form)

  def get_success_url(self):
    return reverse_lazy('users:dashboard')

  def get_context_data(self, **kwargs):
    """Pass context data to generic view."""
    context                       = super(EventEdit, self).get_context_data(**kwargs)
    pk                            = self.kwargs['pk']
    event                         = get_object_or_404(models.Event, pk=pk)
    context['title']              = self.title + (' ') + event.title
    context['form__html_class']   = self.form__html_class
    context['form__action_class'] = 'form-edit'
    context['submit_text']        = _('Guarda los cambios')
    context['object_id']          = pk
    return context

  def get_initial(self):
    super(EventEdit, self).get_initial()
    return {
      "user" : self.request.user
    }

class EventDelete(GenericDelete):
  """Generic view to delete Event objects."""

  model            = models.Event
  title            = _('Borra el evento ')
  form__html_class = 'event'
  success_url      = reverse_lazy('front')
  template_name    = modelform_delete_template

  def get_context_data(self, **kwargs):
    """Pass context data to generic view."""
    context          = super(EventDelete, self).get_context_data(**kwargs)
    pk               = self.kwargs['pk']
    event            = get_object_or_404(models.Event, pk=pk)
    context['title'] = self.title + (' ') + event.title
    context['form__html_class'] = self.form__html_class
    context['question'] = _('¿Estás seguro de que quieres borrar este evento?')
    context['submit_text'] = _('Sí, quiero borrar este evento')
    context['cancel_text'] = _('No, no estoy seguro.')
    return context

  def get_success_url(self):
    return reverse_lazy('users:dashboard')
