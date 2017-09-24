# python
import os
import magic
# django
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class ImageSizeValidator(object):
    """ A validator that checks dimensions of image being loaded. """

    def __init__(self, dimensions=None):
        self.dimensions = dimensions
        self.min_width_error  = _(r"El ancho de la imagen debería ser mayor a %(min_width)s píxeles") % dimensions
        self.max_width_error  = _(r"El ancho de la imagen debería ser menor a %(max_width)s píxeles") % dimensions
        self.min_height_error = _(r"El alto de la imagen debería ser mayor a %(min_height)s píxeles") % dimensions
        self.max_height_error = _(r"El alto de la imagen debería ser menor a %(max_height)s píxeles") % dimensions

    def __call__(self, value):
        errors, width, height = [], value.width, value.height
        if width is not None and width < self.dimensions['min_width']:
            errors.append(self.min_width_error)
        if width is not None and width > self.dimensions['max_width']:
            errors.append(self.max_width_error)
        if height is not None and height < self.dimensions['min_height']:
            errors.append(self.min_height_error)
        if height is not None and height > self.dimensions['max_height']:
            errors.append(self.max_height_error)
        raise ValidationError(errors)

@deconstructible
class ImageTypeValidator(object):

    def __init__(self, mime_types=["jpeg", "png", "gif", "tiff"]):
        self.mime_types = mime_types
        self.type_error = r"La imagen '%(name)s' tiene formato %(format)s. Revise arriba los formatos permitidos"

    def __call__(self, value):
        try:
            mime = magic.from_buffer(value.read(), mime=True)
            mimes = [ ("image/" + mime) for mime in self.mime_types ]
            if mime not in mimes:
                raise ValidationError(_(self.type_error) % { 'name' : value.name, 'format' : mime.split('image/')[1] })
        except ValueError:
            pass
