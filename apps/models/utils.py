# python
import os
# django
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify

@deconstructible
class RenameCivicsImage(object):
    """ An util object to rename images paths when uploading
        It's encapsulated in an object and uses @deconstructible
        to avoid migration problem because of the serialization
        of the object.
        @see https://stackoverflow.com/questions/25767787/django-cannot-create-migrations-for-imagefield-with-dynamic-upload-to-value#25768034 """

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        """ This method has to include instance and filename as parameters
            to be used by django to rename path.
            @see https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.FileField.upload_to """

        subpath = slugify(instance.city.name)
        try:
            filename = slugify(instance.name) + "." + filename.split('.')[1]
        except AttributeError:
            filename = slugify(instance.title) + "." + filename.split('.')[1]

        # return the whole path to the file
        return os.path.join(self.path, subpath, filename)
