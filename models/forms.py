from django.utils.translation import ugettext_lazy as _
from . import models


class CityForm(ModelForm):
  class Meta:
    model = models.City
    widgets = {
        'latlon' : LeafletWidget(),
    }
    fields = '__all__'

class InitiativeForm(ModelForm):
  class Meta:
    model = models.Initiative
    fields = '__all__'
