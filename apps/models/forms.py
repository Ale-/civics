from django.utils.translation import ugettext_lazy as _
from django import forms
from . import models


class CityForm(forms.ModelForm):
  class Meta:
    model = models.City
    fields = '__all__'

class InitiativeForm(forms.ModelForm):
  class Meta:
    model = models.Initiative
    fields = '__all__'

class EventForm(forms.ModelForm):
  class Meta:
    model = models.Event
    fields = '__all__'
