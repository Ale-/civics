from django.db import models
from django.utils.translation import ugettext_lazy as _
from . import geography_utils as geo
from djgeojson.fields import PointField
from leaflet.forms.widgets import LeafletWidget
from . import categories

#
#  City
#
class City(models.Model):
  name    = models.CharField(_('Nombre de la ciudad'), max_length = 200, blank = False, null = True, help_text = _('Especifica el nombre de la ciudad.'))
  country = models.CharField(_('País'), max_length = 2, choices = geo.countries_as_tuple(), blank = False, null = True, help_text = _('¿A qué país pertenece la ciudad?'))
  latlon  = PointField(_("Ubicación"), blank=False, null=True, help_text=_("Añade la ubicación de la ciudad."))

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = _('Ciudad')
    verbose_name_plural = _('Ciudades')

#
#  Initiative
#
class Initiative(models.Model):

  name         = models.CharField(_('Nombre de la iniciativa'), max_length = 200, blank=False, null=True, help_text=_('Especifica el nombre de la iniciativa.'))
  description  = models.TextField(_('Descripción de la iniciativa'), blank=False, null=True, help_text=_('Describe los objetivos y actividad de la iniciativa.'))
  website      = models.URLField(_('Website'), blank=True, null=True, help_text=_('Especifica opcionalmente una web para conocer mejor la iniciativa.'))
  twitter      = models.URLField(_('Twitter'), blank=True, null=True, help_text=_('Describe los objetivos y actividad de la iniciativa.'))
  facebook     = models.URLField(_('Descripción de la iniciativa'), blank=True, null=True, help_text=_('Describe los objetivos y actividad de la iniciativa.'))
  email        = models.EmailField(_('Correo electrónico'), blank=True, null=True, help_text=_('Especifica un correo de contacto para la iniciativa.'))
  topic        = models.TextField(_('Tema'), blank=False, max_length=2, choices = categories.TOPICS, null=True, help_text=_('El tema de la iniciativa'))
  space        = models.TextField(_('Tipo de espacio'), blank=False, max_length=2, choices = categories.SPACES, null=True, help_text=_('El tipo de espacio asociado a la iniciativa'))
  agent        = models.TextField(_('tipo de agente'), blank=False, max_length=2, choices = categories.AGENTS, null=True, help_text=_('El tipo de agente involucrado en la iniciativa'))
  city         = models.ForeignKey(City, blank=False, null=True)
  neighborhood = models.CharField(_('Barrio'), max_length = 200, blank=False, null=True, help_text=_('¿En qué barrio de la ciudad se sitúa la iniciativa?'))
  latlon       = PointField(_("Ubicación"), blank=False, null=True, help_text=_("Añade la ubicación de la iniciativa."))

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = _('Iniciativa')
    verbose_name_plural = _('Iniciativas')
