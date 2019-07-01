# django
from django.utils.translation import ugettext_lazy as _
from django import forms
from django_countries import countries
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.urls import reverse_lazy
from django.utils.text import slugify
# custom
from django.conf import settings
from . import models, categories
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
            'position' : ReducedLeafletWidget(),
        }

    def clean_name(self):
        name   = self.cleaned_data['name']
        cities = models.City.objects.all()
        slugs = [ slugify(city.name) for city in cities ]
        if slugify(name) in slugs:
             raise forms.ValidationError(_('Ya existe una ciudad con ese nombre'))
        return name

class RelationsForm(forms.ModelForm):
    """Modelform to set relationships among initiatives"""

    initiatives = forms.ModelMultipleChoiceField(queryset = models.Initiative.objects.order_by('name'), label=_('Iniciativas relacionadas'),
                                                 help_text=_('Escoge de la columna izquierda las iniciativas relacionadas con la tuya y seleccionalas pasándolas a la columna derecha pulsando el botón "Elegir". '
                                                             'Puedes usar el filtro de la columna izquierda para buscar las iniciativas por su nombre. Ten en cuenta que éste es sensible a mayúsculas, minúsculas y signos de puntuación. '
                                                             'Puedes hacer selecciones múltiples con la tecla Ctrl pulsada (Command en MAC)'),
                                                 required=False,
                                                 widget=FilteredSelectMultiple(_('Elementos'), False,))

    def __init__(self, *args, **kwargs):
        super(RelationsForm, self).__init__(*args, **kwargs)
        self.fields['initiatives'].queryset = models.Initiative.objects.filter(city=self.instance.city).order_by('name')

    class Meta:
        model = models.Initiative
        fields = ['initiatives',]

    class Media:
        js = [
            reverse_lazy('javascript-catalog'),
        ]

    def clean_initiatives(self):
        cleaned_initiatives = self.cleaned_data.get('initiatives')
        if cleaned_initiatives.filter(pk=self.instance.pk).exists():
            raise forms.ValidationError(_('No puedes añadir tu iniciativa a este campo. Seleccionala en la columna derecha y usa el botón "Eliminar" para quitarla de la selección.'))
        return cleaned_initiatives


class InitiativeForm(forms.ModelForm):
    """Generic modelform to create and update Initiative objects"""

    city = GroupedModelChoiceField(queryset=models.City.objects.order_by('country', 'name'),
                                   label=_('Ciudad'),
                                   help_text=_('Ciudad donde se encuentra la iniciativa. Si no encuentras la ciudad en el desplegable usa el botón inferior para añadirla.'),
                                   group_by_field='country', group_label=group_label,
                                   empty_label=" ", widget = SelectOrAddWidget(view_name='modelforms:create_city_popup', link_text=_("Añade una ciudad")))

    class Meta:
        model   = models.Initiative
        exclude  = [ 'initiatives', ]
        widgets = {
            'video'       : VideoWidget(width=640, height=360),
            'image'       : PictureWithPreviewWidget(),
            'description' : LimitedTextareaWidget(limit=500),
        }
        if hasattr(settings, 'GEOCODER_API_KEY'):
            widgets['position'] = GeocodedLeafletWidget(submit_text=_('Localiza la dirección'), provider="google", sources="id_address id_city", key=settings.GEOCODER_API_KEY)
        else:
            widgets['position'] = ReducedLeafletWidget()

    def __init__(self, *args, **kwargs):
        self.base_fields['video'].widget.attrs['placeholder'] = _("Por ejemplo 'https://vimeo.com/45130145'")
        self.base_fields['main_ods'].empty_label = _("Escoge un ODS")
        super(InitiativeForm, self).__init__(*args, **kwargs)

    def clean_video(self):
        video = self.cleaned_data['video']
        if video and not(video.startswith('https://www.youtube.com') or video.startswith('https://vimeo.com') or video.startswith('https://youtu.be')):
             raise forms.ValidationError(_('Las urls admitidas empiezan por "https://www.youtube.com", "https://youtu.be" o "https://vimeo.com"'))
        return video

    def clean(self):
        cleaned_data = super(InitiativeForm, self).clean()
        main_ods  = self.cleaned_data.get('main_ods')
        other_ods = self.cleaned_data.get('other_ods')
        if not main_ods and len(other_ods)>0:
             raise forms.ValidationError(_('Si indicas los ODS de tu iniciativa has de señalar cuál de ellos es el principal.'))
        if main_ods in other_ods:
             raise forms.ValidationError(_('No repitas el objetivo principal de tu iniciativa en el campo "Otros ODS".'))
        if len(other_ods) > 3:
             raise forms.ValidationError(_('Indica un máximo de tres objetivos.'))
        website  = cleaned_data.get("website")
        twitter  = cleaned_data.get("twitter")
        facebook = cleaned_data.get("facebook")
        if not website and not twitter and not facebook:
            raise forms.ValidationError(_("Has de proporcionar la url de una página web o de un perfil público de una red social para poder añadir tu iniciativa."))
        return self.cleaned_data


class EventForm(forms.ModelForm):
    """Generic modelform to create and update Event objects"""

    city = GroupedModelChoiceField(queryset=models.City.objects.order_by('country', 'name'),
                                   label=_('Ciudad'),
                                   help_text=_('Ciudad donde se celebra el evento. Si no encuentras la ciudad en el desplegable usa el botón inferior para añadirla.'),
                                   group_by_field='country', group_label=group_label,
                                   empty_label=" ", widget = SelectOrAddWidget(view_name='modelforms:create_city_popup', link_text=_("Añade una ciudad")) )

    class Meta:
        model = models.Event
        fields = '__all__'
        widgets = {
            'video'       : VideoWidget(),
            'image'       : PictureWithPreviewWidget(),
            'description' : LimitedTextareaWidget(limit=500),
        }
        if hasattr(settings, 'GEOCODER_API_KEY'):
            widgets['position'] = GeocodedLeafletWidget(submit_text=_('Localiza la dirección'), provider="google", sources="id_address id_city", key=settings.GEOCODER_API_KEY)
        else:
            widgets['position'] = ReducedLeafletWidget()

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
