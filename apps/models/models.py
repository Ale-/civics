# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
# contrib
from imagekit.models import ImageSpecField
from imagekit import processors
from leaflet.forms.widgets import LeafletWidget
from django_countries.fields import CountryField
from djgeojson.fields import PointField
# project
from . import categories
from .validators import ImageTypeValidator, ImageSizeValidator, AttachedFileValidator
from .utils import RenameCivicsImage


# Bound methods moved from model to avoid problems with serialization in migrations

validate_image_size     = ImageSizeValidator({ 'min_width' : 600, 'min_height' : 300, 'max_width' : 1920, 'max_height' : 1280 })
validate_image_type     = ImageTypeValidator(["jpeg", "png"])
validate_file_type     = AttachedFileValidator()
initiatives_images_path = RenameCivicsImage("images/initiatives/")
events_images_path      = RenameCivicsImage("images/events/")

#
# ODS
#
class ODS(models.Model):
  """Model to represent ODS categories"""

  category = models.CharField(_('Objetivo de desarrollo sostenible'), choices=categories.ODS, default=1, max_length=2, blank=False)
  order    = models.PositiveSmallIntegerField(_('Orden'), default=1)

  def __str__(self):
    """String representation of this model objects."""
    return "[%s] %s" % (self.order, self.get_category_display())

  class Meta:
    verbose_name = _('ODS')
    verbose_name_plural = _('ODS')
    ordering = [ 'order' ]

#
#  City
#

class City(models.Model):
  """Model to represent City objects"""

  name               = models.CharField(_('Nombre de la ciudad'), max_length = 200, blank = False, null = True,
                       help_text = _('Especifica el nombre de la ciudad en español.'))
  name_pt            = models.CharField(_('Nombre de la ciudad (PT)'), max_length = 200, blank = False, null = True,
                       help_text = _('Especifica el nombre de la ciudad en portugúes si es distinto al nombre español.'))
  name_en            = models.CharField(_('Nombre de la ciudad (EN)'), max_length = 200, blank = False, null = True,
                       help_text = _('Especifica el nombre de la ciudad en inglés si es distinto al nombre español.'))
  country            = CountryField(_('País'), null=True, help_text = _('¿A qué país pertenece la ciudad?'))
  position           = PointField(_("Ubicación"), blank=False, null=True, help_text=_("Añade la ubicación de la ciudad."))
  initiative_related = models.BooleanField(default=False)
  event_related      = models.BooleanField(default=False)

  def translated_name(self, langcode):
      namefield = 'name_' + langcode
      if langcode != 'es' and getattr(self, namefield):
          return getattr(self, namefield)
      return self.name

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
  image         = models.ImageField(_("Imagen"), blank=True,
                                    validators=[validate_image_size, validate_image_type],
                                    upload_to  = initiatives_images_path,
                                    help_text=_("Sube una imagen representativa de la iniciativa haciendo click en la imagen inferior. "
                                                "La imagen ha de tener ancho mínimo de 600 píxeles y máximo de 1920, y altura mínima "
                                                "de 300 píxeles y máxima de 1280. Formatos permitidos: PNG, JPG, JPEG."))
  image_medium = ImageSpecField(source="image", processors=[processors.ResizeToFill(600, 300)], format='JPEG', options={'quality': 90})
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
  email         = models.EmailField(_('Correo electrónico'), blank=False, null=True,
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
  # ODS
  main_ods      = models.ForeignKey(ODS, verbose_name=_('Objetivo de desarrollo sostenible principal'), blank=True, null=True,
                                    help_text=_('Indícanos que Objetivo de Desarrollo Sostenible (ODS) crees que cumple o trabaja principalmente tu iniciativa.'))
  other_ods     = models.ManyToManyField(ODS, verbose_name=_('Otros ODS'), blank=True, related_name='initiatives',
                                    help_text=_('Indícanos otros Objetivos de Desarrollo Sostenible (ODS) con los que también trabaja tu iniciativa (máximo 3). Puedes deseleccionar y hacer selecciones múltiples usando el ratón con la tecla Ctrl pulsada (Command en MAC)'))

  # Relations
  initiatives   = models.ManyToManyField('self', verbose_name=_('Relaciones'), blank=True)
  file          = models.FileField(
    _('Archivo adjunto'),
    upload_to='files/initiatives',
    blank=True,
    validators=[validate_file_type],
    help_text=_(
        'Puedes usar este campo para subir algún documento que explique '
        'mejor tu iniciativa. Sólo admite formato PDF.'
    )
  )


  class Meta:
    verbose_name        = _('Iniciativa')
    verbose_name_plural = _('Iniciativas')

  def __str__(self):
    """String representation of this model objects."""
    return self.name or '---'

  @property
  def translated_name(self):
      print(self.request)

  @property
  def external_url(self):
    """Returns the first occurence of an external url related to the initiative"""
    if self.website:
        return self.website
    elif self.facebook:
        return self.facebook
    return "https://twitter.com/" + self.twitter

  def save(self, *args, **kwargs):
    """Populate automatically 'slug' field"""
    self.slug = slugify(self.name)
    # Notify by mail, only when creating new content
    if not self.id:
        send_mail( 'Creada la iniciativa \"' + self.name + "\"",
            'Creada el ' + self.creation_date.strftime("%d/%b/%Y") + ' por ' + self.user.username + '\n---\n' +
            self.name + ' (' + self.email + '):\n' +
            self.description + '\n---\n' +
            'Ciudad: ' + self.city.name,
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
  image         = models.ImageField(_("Imagen"), blank=True,
                                    validators=[validate_image_size, validate_image_type],
                                    upload_to  = events_images_path,
                                    help_text=_("Sube una imagen representativa del evento haciendo click en la imagen inferior. "
                                                "La imagen ha de tener ancho mínimo de 600 píxeles y máximo de 1920, y altura mínima "
                                                "de 300 píxeles y máxima de 1280. Formatos permitidos: PNG, JPG, JPEG."))
  image_medium = ImageSpecField(source="image", processors=[processors.ResizeToFill(600, 300)], format='JPEG', options={'quality': 90})
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
                                  help_text=_('Indica qué día se celebra o empieza el evento'))
  time         = models.TimeField(_('Hora del evento'),
                                  help_text=_('¿A qué hora se celebra el evento?'))
  periodicity  = models.CharField(_('Periodicidad'), max_length = 200, blank=True, null=True,
                                  help_text=_('Especifica, en ese caso, la periodicidad del evento. Puedes indicar la fecha de fin en el siguiente campo'))
  expiration   = models.DateField(_('Fecha de fin'), blank=True, null=True,
                                  help_text=_('Indica opcionalmente en eventos de varios dias la fecha en que acaba el evento.'))
  city         = models.ForeignKey(City, verbose_name=_('Ciudad'), blank=False, null=True, on_delete=models.SET_NULL,
                                     help_text=_('Ciudad donde se encuentra la iniciativa. Si no la encuentras en la lista puedes añadir una nueva.'))
  address      = models.CharField(_('Dirección'), max_length = 200, blank=False, null=True,
                                   help_text=_('Dirección de la iniciativa. No es necesario que vuelvas a introducir la ciudad de la iniciativa.'))
  position     = PointField(_("Ubicación"), blank=False, null=True,
                            help_text=_("Añade la ubicación de la actividad. Si lo dejas en blanco se usará la ubicación de la iniciativa asociada."))
  facebook_id  = models.CharField(max_length=128, blank=True, null=True)
  google_id    = models.CharField(max_length=128, blank=True, null=True)
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
        send_mail( 'Creado el evento \"' + self.title + "\"",
            'Creado el ' + self.creation_date.strftime("%d/%b/%Y") + ' por "' + self.initiative.name +
            '" (' + self.initiative.email + ')\n---\n' +
            self.title + ':\n' +
            self.description + '\n---\n' +
            'Ciudad: ' + self.city.name,
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

class Resource(models.Model):

    name = models.CharField(
        _('Nombre del recurso'),
        max_length = 200,
        blank=False,
        null=True,
    )
    name_en = models.CharField(
        _('Nombre del recurso en inglés'),
        max_length = 200,
        blank=False,
        null=True,
    )
    name_pt = models.CharField(
        _('Nombre del recurso en portugués'),
        max_length = 200,
        blank=False,
        null=True,
    )
    category = models.CharField(
        _('Tipo de recurso'),
        blank=False,
        null=False,
        default='0',
        max_length=2,
        choices = categories.RESOURCES,
    )
    image = models.ImageField(
        _("Imagen"),
        blank=True,
        validators=[validate_image_size, validate_image_type],
        upload_to='images/resources',
    )
    file = models.FileField(
        _("Archivo"),
        blank=True,
        upload_to='files/resources',
    )
    url = models.URLField(
        _("Enlace"),
        blank=True,
        help_text=_('Si el recurso es un site externo puedes indicar la url aquí.')
    )
    summary = models.TextField(
        _('Descripción corta del recurso'),
        blank=False,
        null=True,
    )
    summary_en = models.TextField(
        _('Descripción corta del recurso [inglés]'),
        blank=False,
        null=True,
    )
    summary_pt = models.TextField(
        _('Descripción corta del recurso [portugués]'),
        blank=False,
        null=True,
    )

    def __str__(self):
        """String representation of this model objects."""
        return self.name

    def get_name(self, lang):
        return self.name if lang==settings.LANGUAGE_CODE else getattr(self, 'name_'+lang)

    def get_summary(self, lang):
        return self.summary if lang==settings.LANGUAGE_CODE else getattr(self, 'summary_'+lang)
