from django.utils.translation import ugettext_lazy as _
from django import forms
from . import models
from apps.utils.fields import GroupedModelChoiceField
from leaflet.forms.widgets import LeafletWidget


class CityForm(forms.ModelForm):
    """Generic modelform to create and update City objects"""

    class Meta:
        model = models.City
        fields = '__all__'

class InitiativeForm(forms.ModelForm):
    """Generic modelform to create and update Initiative objects"""

    def group_label(country_key):
        return dict(models.COUNTRIES)[country_key]

    city = GroupedModelChoiceField(queryset=models.City.objects.order_by('country', 'name'),
                                   group_by_field='country', group_label=group_label,
                                   empty_label="")

    class Meta:
        model   = models.Initiative
        fields  = '__all__'
        widgets = {
            'position' : LeafletWidget(),
        }

    def __init__(self, *args, **kwargs):
        self.base_fields['user'].widget.attrs['disabled'] = True
        self.base_fields['user'].widget.attrs['readonly'] = True
        self.base_fields['user'].initial = kwargs['initial']['user']
        self.base_fields['email'].initial = kwargs['initial']['user'].email
        super(InitiativeForm, self).__init__(*args, **kwargs)

class EventForm(forms.ModelForm):
    """Generic modelform to create and update Event objects"""

    class Meta:
        model = models.Event
        fields = '__all__'
