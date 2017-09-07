from django.db import models
from django.utils.translation import ugettext_lazy as _
from . import categories
from djgeojson.fields import PointField
from leaflet.forms.widgets import LeafletWidget
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToCover
from django_countries.fields import CountryField
from django.core.mail import send_mail
from django.conf import settings

#
#  City
#

class City(models.Model):
  """Model to represent City objects"""

  name     = models.CharField(_('Nombre de la ciudad'), max_length = 200, blank = False, null = True,
                              help_text = _('Especifica el nombre de la ciudad.'))
  country = CountryField(_('País'), null=True, help_text = _('¿A qué país pertenece la ciudad?'))
  position = PointField(_("Ubicación"), blank=False, null=True, help_text=_("Añade la ubicación de la ciudad."))

  class Meta:
    verbose_name = _('Ciudad')
    verbose_name_plural = _('Ciudades')

  def __str__(self):
    """String representation of this model objects."""
    return self.name or '---'


#
#  Initiative
#

class Initiative(models.Model):
  """Model to represent Initiative objects"""

  name          = models.CharField(_('Nombre de la iniciativa'), max_length=200, blank=False, null=True,
                                   help_text=_('¿Cuál es el nombre de tu iniciativa?'))
  slug          = models.SlugField(editable=False, blank=True)
  creation_date = models.DateField(editable=False, default=timezone.now)
  featured      = models.BooleanField(_('Destacado'), blank=True, default=False,
                                     help_text=_('Indica si es una iniciativa destacada'))
  user          = models.ForeignKey(User, verbose_name=_('Gestor'), blank=True, null=True, on_delete=models.SET_NULL)
  image         = models.ImageField(_("Imagen"), blank=True, upload_to="images/initiatives/",
                                    help_text=_("Sube una imagen representativa de la iniciativa haciendo click en la imagen inferior."))
  image_medium = ImageSpecField(source="image", processors=[ResizeToFill(600, 300)], format='JPEG', options={'quality': 90})
  video         = models.CharField(_('Video'), max_length=200, blank=True, null=True,
                                   help_text=_('Inserta la url de un video de Youtube o Vimeo'))
  description   = models.TextField(_('Descripción de la iniciativa'), blank=False, null=True,
                                   help_text=_('Describe los objetivos y actividad de la iniciativa.'))
  website       = models.URLField(_('Website'), blank=True, null=True,
                                   help_text=_('Especifica opcionalmente una web para conocer mejor la iniciativa.'))
  twitter       = models.CharField(_('Twitter'), blank=True, null=True, max_length = 128,
                                   help_text=_('Si tienes una cuenta de Twitter, pon aquí el nombre de usuario.'))
  facebook      = models.URLField(_('Facebook'), blank=True, null=True,
                                  help_text=_('Si tienes un perfil de Facebook pon aquí el enlace completo a la misma.'))
  email         = models.EmailField(_('Correo electrónico'), blank=True, null=True,
                                    help_text=_('Especifica un correo de contacto para la iniciativa.'))
  topic         = models.CharField(_('Tema'), blank=False, null=False, default='DC', max_length=2, choices = categories.TOPICS,
                                    help_text=_('El tema de la iniciativa'))
  space         = models.CharField(_('Tipo de espacio'), blank=False, null=False, default='CC', max_length=2, choices = categories.SPACES,
                                   help_text=_('El tipo de espacio asociado a la iniciativa'))
  agent         = models.CharField(_('tipo de agente'), blank=False, null=False, default='IM', max_length=2, choices = categories.AGENTS,
                                   help_text=_('El tipo de agente involucrado en la iniciativa'))
  city          = models.ForeignKey(City, verbose_name=_('Ciudad'), blank=False, null=True, on_delete=models.SET_NULL,
                                    help_text=_('Ciudad donde se encuentra la iniciativa. Si no encuentras la ciudad en el desplegable usa el botón inferior para añadir una nueva ciudad y seleccionarla'))
  address       = models.CharField(_('Dirección'), max_length = 200, blank=False, null=True,
                                   help_text=_('Dirección de la iniciativa. No es necesario que vuelvas a introducir la ciudad de la iniciativa.'))
  district      = models.CharField(_('Distrito'), max_length = 200, blank=True, null=True,
                                   help_text=_('¿En qué barrio de la ciudad se sitúa la iniciativa?'))
  position      = PointField(_("Ubicación"), blank=False, null=True,
                             help_text=_("Tras añadir ciudad y dirección puedes ubicar la iniciativa pulsando el botón inferior y ajustando la posición del marcador posteriormente."))

  class Meta:
    verbose_name        = _('Iniciativa')
    verbose_name_plural = _('Iniciativas')

  def __str__(self):
    """String representation of this model objects."""
    return self.name or '---'

  def save(self, *args, **kwargs):
    """Populate automatically 'slug' field"""
    self.slug = slugify(self.name)
    # Notify by mail, only when creating new content
    if not self.id:
        send_mail( 'Se ha creado una iniciativa nueva en civics.cc: ' + str(self.name),
            'El ' + str(self.creation_date) + ' se creó la iniciativa ' + str(self.name) + '.',
            'civics.cc <no-reply@civics.cc>',
            settings.NOTIFICATIONS_EMAILS,
            fail_silently=False,
        );
    super(Initiative, self).save(*args, **kwargs)

  def edit_permissions(self, user):
    """Returns users allowed to edit an instance of this model."""
    if user.is_staff or (self.user and self.user == user):
      return True
    return False


#
#  Event
#

class Event(models.Model):
  """Model to represent Event objects"""

  initiative   = models.ForeignKey(Initiative, verbose_name=_("Iniciativa que organiza la actividad"), blank=True, null=True,
                                   help_text=_('¿Qué iniciativa organiza el evento?'))
  title        = models.CharField(_('Título del evento'), max_length = 200, blank=False, null=True,
                                  help_text=_('¿Cuál es el título del evento que quieres organiza?'))
  featured     = models.BooleanField(_('Destacado'), blank=True, default=False,
                                     help_text=_('Indica si es un evento destacado'))
  description  = models.TextField(_('Describe el evento'), blank=False, null=True,
                                  help_text=_('Describe el evento.'))
  image        = models.ImageField(_("Imagen"), blank=True, upload_to="images/initiatives/",
                                    help_text=_("Sube una imagen representativa del evento"))
  image_medium = ImageSpecField(source="image", processors=[ResizeToFill(600, 300)], format='JPEG', options={'quality': 90})
  thumbnail    = ImageSpecField(source="image", processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 90})
  video        = models.CharField(_('Video'), max_length=200, blank=True, null=True,
                                   help_text=_('Inserta la url de un video de Youtube o Vimeo'))
  website      = models.URLField(_('Enlace'), blank=True, null=True,
                                   help_text=_('Especifica opcionalmente un enlace para conocer mejor el evento.'))
  topic        = models.CharField(_('Temática del evento'), blank=False, null=False, default='DC', max_length=2, choices = categories.TOPICS,
                                   help_text=_('El tema de la actividad'))
  category     = models.CharField(_('Tipo de actividad'), blank=False, null=False, default='AU', max_length=2, choices = categories.ACTIVITIES,
                                  help_text=_('El tipo de actividad que quieres organizar'))
  agent        = models.CharField(_('tipo de agente'), blank=False, null=False, default='IM', max_length=2, choices = categories.AGENTS,
                                  help_text=_('El tipo de agente involucrado en la actividad'))
  date         = models.DateField(_('Fecha del evento'),
                                  help_text=_('¿Qué día se celebra el evento?'))
  time         = models.TimeField(_('Hora del evento'),
                                  help_text=_('¿A qué hora se celebra el evento?'))
  periodicity  = models.CharField(_('Periodicidad'), max_length=2, choices=categories.PERIODICITY, blank=True, null=True,
                                  help_text=_('Especifica, en ese caso, la periodicidad del evento.'))
  city         = models.ForeignKey(City, verbose_name=_('Ciudad'), blank=False, null=True, on_delete=models.SET_NULL,
                                     help_text=_('Ciudad donde se encuentra la iniciativa. Si no la encuentras en la lista puedes añadir una nueva.'))
  address      = models.CharField(_('Dirección'), max_length = 200, blank=False, null=True,
                                   help_text=_('Dirección de la iniciativa. No es necesario que vuelvas a introducir la ciudad de la iniciativa.'))
  position     = PointField(_("Ubicación"), blank=False, null=True,
                            help_text=_("Añade la ubicación de la actividad. Si lo dejas en blanco se usará la ubicación de la iniciativa asociada."))
  facebook_id  = models.PositiveIntegerField(blank=True, null=True)

  slug          = models.SlugField(editable=False, blank=True)
  creation_date = models.DateField(editable=False, default=timezone.now)

  class Meta:
    verbose_name = _('Actividad')
    verbose_name_plural = _('Actividades')

  def __str__(self):
    """String representation of this model objects."""
    return self.title or '---'

  def save(self, *args, **kwargs):
    """Populate automatically 'slug' field"""
    self.slug = slugify(self.title)
    # Notify by mail, only when creating new content
    if not self.id:
        send_mail( 'Se ha creado un evento nuevo en civics.cc: ' + str(self.title),
            'El ' + str(self.creation_date) + ' se creó el evento ' + str(self.title) + '.',
            'civics.cc <no-reply@civics.cc>',
            settings.NOTIFICATIONS_EMAILS,
            fail_silently=False,
        );
    super(Event, self).save(*args, **kwargs)

  def edit_permissions(self, user):
    """Returns users allowed to edit an instance of this model."""
    if user.is_staff or (self.initiative and self.initiative.user and self.initiative.user == user):
        return True
    return False
