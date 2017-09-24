# django
from django.core.serializers.json import Serializer

class CivicsJSONSerializer(Serializer):
    def get_dump_object(self, obj):
        data = self._current
        data['image'] = obj.image_medium.url if obj.image_medium else None
        data['pk'] = obj.pk
        return data
