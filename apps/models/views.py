from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from apps.utils.views import GenericCreate, GenericUpdate, GenericDelete
from . import forms, models
from django.urls import reverse_lazy

# Model related views

modelform_generic_template = 'pages/modelform.html'

#
#  City
#

class CityCreate(GenericCreate):
  """ Generic view to create City objects """

  model = models.City
  form_class = forms.CityForm
  template_name = modelform_generic_template
  title = _('Añade una ciudad')
  success_url = reverse_lazy('front')

class CityEdit(GenericUpdate):
  """ Generic view to edit City objects """

  model = models.City
  form_class = forms.CityForm
  template_name = modelform_generic_template
  title = _('Edita la información de ')
  success_url = reverse_lazy('front')

  def get_context_data(self, **kwargs):
    context          = super(CityEdit, self).get_context_data(**kwargs)
    id               = self.kwargs['pk']
    city             = get_object_or_404(models.City, pk=pk)
    context['title'] = self.title + (' ') + receiver.name
    return context

class CityDelete(GenericDelete):
  """ Generic view to delete City objects """

  model = models.City
  form_class = forms.CityForm
  template_name = modelform_generic_template
  title = _('Borra la ciudad ')
  success_url = reverse_lazy('front')

  def get_context_data(self, **kwargs):
    context          = super(CityEdit, self).get_context_data(**kwargs)
    id               = self.kwargs['pk']
    city             = get_object_or_404(models.City, pk=pk)
    context['title'] = self.title + (' ') + receiver.name
    return context


#
#  Initiative
#

class InitiativeCreate(GenericCreate):
  """ Generic view to create Initiative objects """

  model = models.Initiative
  form_class = forms.InitiativeForm
  template_name = modelform_generic_template
  title = _('Añade una iniciativa')
  success_url = reverse_lazy('front')

class InitiativeEdit(GenericUpdate):
  """ Generic view to edit Initiative objects """
  model = models.Initiative
  form_class = forms.InitiativeForm
  template_name = modelform_generic_template
  title = _('Edita la información de la iniciativa ')
  success_url = reverse_lazy('front')

  def get_context_data(self, **kwargs):
    context          = super(InitiativeEdit, self).get_context_data(**kwargs)
    slug             = self.kwargs['slug']
    initiative       = get_object_or_404(models.Initiative, slug=slug)
    context['title'] = self.title + (' ') + initiative.name
    return context

class InitiativeDelete(GenericDelete):
  """ Generic view to delete Initiative objects """
  model = models.Initiative
  form_class = forms.InitiativeForm
  template_name = modelform_generic_template
  title = _('Borra la iniciativa ')
  success_url = reverse_lazy('front')

  def get_context_data(self, **kwargs):
    context          = super(InitiativeDelete, self).get_context_data(**kwargs)
    slug             = self.kwargs['slug']
    initiative       = get_object_or_404(models.Initiative, slug=slug)
    context['title'] = self.title + (' ') + initiative.name
    return context

#
#  Event
#

class EventCreate(GenericCreate):
  """ Generic view to create Event objects """

  model = models.Event
  form_class = forms.EventForm
  template_name = modelform_generic_template
  title = _('Crea un evento ')
  success_url = reverse_lazy('front')

class EventEdit(GenericUpdate):
  """ Generic view to edit Event objects """
  model = models.Event
  form_class = forms.EventForm
  template_name = modelform_generic_template
  title = _('Edita la información del evento ')
  success_url = reverse_lazy('front')


  def get_context_data(self, **kwargs):
    context          = super(EventEdit, self).get_context_data(**kwargs)
    slug             = self.kwargs['slug']
    event            = get_object_or_404(models.City, slug=slug)
    context['title'] = self.title + (' ') + event.name
    return context

class EventDelete(GenericDelete):
  """ Generic view to delete Event objects """

  model = models.Event
  title = _('Borra el evento ')
  success_url = reverse_lazy('front')
  template_name = modelform_generic_template

  def get_context_data(self, **kwargs):
    context          = super(EventDelete, self).get_context_data(**kwargs)
    slug             = self.kwargs['slug']
    event            = get_object_or_404(models.Event, slug=slug)
    context['title'] = self.title + (' ') + event.name
    return context
