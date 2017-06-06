from django.utils.translation import ugettext_lazy as _
from django import forms
from . import models
from apps.utils.fields import GroupedModelChoiceField
from apps.utils.widgets import VideoWidget, PictureWithPreviewWidget, ReducedLeafletWidget, LimitedTextareaWidget, SelectOrAddWidget, GeocodedLeafletWidget


def group_label(country_key):
    return dict(models.COUNTRIES)[country_key]

class CityForm(forms.ModelForm):
    """Generic modelform to create and update City objects"""

    class Meta:
        model = models.City
        fields = '__all__'
        widgets = {
            'position'    : ReducedLeafletWidget(),
        }


class InitiativeForm(forms.ModelForm):
    """Generic modelform to create and update Initiative objects"""

    city = GroupedModelChoiceField(queryset=models.City.objects.order_by('country', 'name'),
                                   label='Ciudad',
                                   help_text=_('Ciudad donde se encuentra la iniciativa. Si no encuentras la ciudad en el desplegable usa el botón inferior para añadirla.'),
                                   group_by_field='country', group_label=group_label,
                                   empty_label=" ", widget = SelectOrAddWidget(view_name='modelforms:create_city_popup', link_text=_("Añade una ciudad")) )

    class Meta:
        model   = models.Initiative
        fields  = '__all__'
        widgets = {
            'position'    : GeocodedLeafletWidget(submit_text='Localiza la dirección de la iniciativa', provider="google", sources="id_address id_city"),
            'video'       : VideoWidget(width=640, height=360),
            'image'       : PictureWithPreviewWidget(),
            'description' : LimitedTextareaWidget(limit=500),
        }

    def __init__(self, *args, **kwargs):
        self.base_fields['user'].widget.attrs['readonly'] = True
        self.base_fields['video'].widget.attrs['placeholder'] = _("Por ejemplo 'https://vimeo.com/45130145'")
        if('user' in kwargs['initial']):
            self.base_fields['user'].initial = kwargs['initial']['user']
            self.base_fields['email'].initial = kwargs['initial']['user'].email
        super(InitiativeForm, self).__init__(*args, **kwargs)


class EventForm(forms.ModelForm):
    """Generic modelform to create and update Event objects"""

    def group_label(country_key):
        return dict(models.COUNTRIES)[country_key]

    city = GroupedModelChoiceField(queryset=models.City.objects.order_by('country', 'name'),
                                   label='Ciudad',
                                   help_text=_('Ciudad donde se celebra el evento. Si no encuentras la ciudad en el desplegable usa el botón inferior para añadirla.'),
                                   group_by_field='country', group_label=group_label,
                                   empty_label=" ", widget = SelectOrAddWidget(view_name='modelforms:create_city_popup', link_text=_("Añade una ciudad")) )

    class Meta:
        model = models.Event
        fields = '__all__'
        widgets = {
            'position'    : GeocodedLeafletWidget(submit_text='Localiza la dirección de la iniciativa', provider="google", sources="id_address id_city"),
            'video'       : VideoWidget(),
            'image'       : PictureWithPreviewWidget(),
        }

    def __init__(self, *args, **kwargs):
        self.base_fields['image'].widget.attrs['accept'] = 'image/*'
        self.base_fields['date'].widget.attrs['placeholder'] = _("Usa el formato dd/mm/aaaa, por ejemplo '05/06/2017'")
        self.base_fields['time'].widget.attrs['placeholder'] = _("Usa el formato hh:mm, por ejemplo '09:00'")
        self.base_fields['video'].widget.attrs['placeholder'] = _("Por ejemplo 'https://vimeo.com/45130145'")
        super(EventForm, self).__init__(*args, **kwargs)
