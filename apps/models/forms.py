# django
from django.utils.translation import ugettext_lazy as _
from django import forms
from django_countries import countries
from django.core.exceptions import ValidationError
# custom
from . import models
from apps.utils.fields import GroupedModelChoiceField
from apps.utils.widgets import VideoWidget, PictureWithPreviewWidget, ReducedLeafletWidget, LimitedTextareaWidget, SelectOrAddWidget, GeocodedLeafletWidget

def group_label(country_key):
    if country_key:
        return dict(countries)[country_key]
    return None

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
                                   label=_('Ciudad'),
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
        self.base_fields['video'].widget.attrs['placeholder'] = _("Por ejemplo 'https://vimeo.com/45130145'")
        super(InitiativeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(InitiativeForm, self).clean()
        website  = cleaned_data.get("website")
        twitter  = cleaned_data.get("twitter")
        facebook = cleaned_data.get("facebook")
        if not website and not twitter and not facebook:
            raise forms.ValidationError(_("Has de proporcionar la url de una página web o de un perfil público de una red social para poder añadir tu iniciativa."))



class EventForm(forms.ModelForm):
    """Generic modelform to create and update Event objects"""

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
            'description' : LimitedTextareaWidget(limit=500),
        }

    def __init__(self, *args, **kwargs):
        self.base_fields['image'].widget.attrs['accept'] = 'image/*'
        self.base_fields['date'].widget.attrs['placeholder'] = _("Usa el formato dd/mm/aaaa, por ejemplo '05/06/2017'")
        self.base_fields['expiration'].widget.attrs['placeholder'] = _("Usa el formato dd/mm/aaaa, por ejemplo '05/06/2017'")
        self.base_fields['periodicity'].widget.attrs['placeholder'] = _("P.ej. 'Todos los martes' o 'Cada dos semanas'")
        self.base_fields['time'].widget.attrs['placeholder'] = _("Usa el formato hh:mm, por ejemplo '09:00'")
        self.base_fields['video'].widget.attrs['placeholder'] = _("Por ejemplo 'https://vimeo.com/45130145'")
        # Check if initial for ajax form in user's dashboard
        if 'initial' in kwargs and 'user' in kwargs['initial']:
            user = kwargs['initial']['user']
            if not user.is_staff:
                self.base_fields['initiative'].queryset = models.Initiative.objects.filter(user=user).order_by('name')
            else:
                self.base_fields['initiative'].queryset = models.Initiative.objects.order_by('name')
        self.base_fields['initiative'].empty_label = None
        super(EventForm, self).__init__(*args, **kwargs)
