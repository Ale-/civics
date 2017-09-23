# python
import os
import magic
import datetime
# django
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.text import slugify

def initiative_rename(path):
    """ A custom function to rename image files once uploaded"""

    def rename(instance, filename):
        date = datetime.datetime.now()
        subpath = instance.city.name
        filename = slugify(instance.name) + "." + filename.split('.')[1]
        return os.path.join(path, subpath, filename)

    return rename

def event_rename(path):
    """ A custom function to rename image files once uploaded"""

    def rename(instance, filename):
        date = datetime.datetime.now()
        subpath = instance.city.name
        filename = slugify(instance.title) + "." + filename.split('.')[1]
        return os.path.join(path, subpath, filename)

    return rename

def image_size(min_width=None, min_height=None, max_width=None, max_height=None):
    """ A custom to validator to check image dimensions in forms."""

    min_width_error  = r"El ancho de la imagen debería ser mayor a %(min_width)s píxeles"
    max_width_error  = r"El ancho de la imagen debería ser menor a %(max_width)s píxeles"
    min_height_error = r"El alto de la imagen debería ser mayor a %(min_height)s píxeles"
    max_height_error = r"El alto de la imagen debería ser menor a %(max_height)s píxeles"
    params = {
        'min_width'  : min_width,
        'max_width'  : max_width,
        'min_height' : min_height,
        'max_height' : max_height,
    }

    def validator(image):
        errors, width, height = [], image.width, image.height
        if width is not None and width < min_width:
            errors.append(_(min_width_error) % params)
        if width is not None and width > max_width:
            errors.append(_(max_width_error) % params)
        if height is not None and height < min_height:
            errors.append(_(min_height_error) % params)
        if height is not None and height > max_height:
            errors.append(_(max_height_error) % params)
        raise ValidationError(errors)

    return validator


def image_type(mime_types=["jpeg", "png", "gif", "tiff"]):

    type_error = r"La imagen '%(name)s' tiene formato %(format)s. Revise arriba los formatos permitidos"

    def validator(image):
        try:
            mime = magic.from_buffer(image.read(), mime=True)
            mimes = [ ("image/" + mime) for mime in mime_types ]
            if mime not in mimes:
                raise ValidationError(type_error % { 'name' : image.name, 'format' : mime.split('image/')[1] })
        except ValueError:
            pass

    return validator
