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
  name     = models.CharField(_('Nombre de la ciudad'), max_length = 200, blank = False, null = True, help_text = _('Especifica el nombre de la ciudad.'))
  country  = models.CharField(_('País'), max_length = 2, choices = geo.countries_as_tuple(), blank = False, null = True, help_text = _('¿A qué país pertenece la ciudad?'))
  position = PointField(_("Ubicación"), blank=False, null=True, help_text=_("Añade la ubicación de la ciudad."))

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = _('Ciudad')
    verbose_name_plural = _('Ciudades')

#
#  Initiative
#
class Initiative(models.Model):

  name         = models.CharField(_('Nombre de la iniciativa'), max_length = 200, blank=False, null=True,
                                  help_text=_('¿Cuál es el nombre de tu iniciativa?'))
  description  = models.TextField(_('Descripción de la iniciativa'), blank=False, null=True,
                                  help_text=_('Describe los objetivos y actividad de la iniciativa.'))
  website      = models.URLField(_('Website'), blank=True, null=True,
                                  help_text=_('Especifica opcionalmente una web para conocer mejor la iniciativa.'))
  twitter      = models.CharField(_('Twitter'), blank=True, null=True,
                                  help_text=_('Si tienes una cuenta de Twitter, pon aquí el nombre del usuario sin la @ inicial.'))
  facebook     = models.URLField(_('Descripción de la iniciativa'), blank=True, null=True,
                                 help_text=_('Describe los objetivos y actividad de la iniciativa.'))
  email        = models.EmailField(_('Correo electrónico'), blank=True, null=True,
                                   help_text=_('Especifica un correo de contacto para la iniciativa.'))
  topic        = models.CharField(_('Tema'), blank=False, null=False, default='DC', max_length=2, choices = categories.TOPICS,
                                   help_text=_('El tema de la iniciativa'))
  space        = models.CharField(_('Tipo de espacio'), blank=False, null=False, default='CC', max_length=2, choices = categories.SPACES,
                                  help_text=_('El tipo de espacio asociado a la iniciativa'))
  agent        = models.CharField(_('tipo de agente'), blank=False, null=False, default='IM', max_length=2, choices = categories.AGENTS,
                                  help_text=_('El tipo de agente involucrado en la iniciativa'))
  city         = models.ForeignKey(City, blank=False, null=True)
  address      = models.CharField(_('Dirección'), max_length = 200, blank=False, null=True,
                                  help_text=_('Dirección de la iniciativa'))
  district     = models.CharField(_('Distrito'), max_length = 200, blank=False, null=True,
                                  help_text=_('¿En qué barrio de la ciudad se sitúa la iniciativa?'))
  position     = PointField(_("Ubicación"), blank=False, null=True,
                            help_text=_("Añade la ubicación de la iniciativa."))

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = _('Iniciativa')
    verbose_name_plural = _('Iniciativas')
