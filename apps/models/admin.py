# django
from django.contrib import admin

# contrib
from leaflet.admin import LeafletGeoAdmin
from imagekit import ImageSpec
from imagekit.admin import AdminThumbnail
from imagekit.processors import ResizeToFill
from imagekit.cachefiles import ImageCacheFile

# project
from . import models


# Custom actions
def feature(modeladmin, request, queryset):
    queryset.update(featured=True)

feature.short_description = "Destaca los proyectos seleccionados"

def unfeature(modeladmin, request, queryset):
    queryset.update(featured=False)

unfeature.short_description = "Dejar de destacar de los proyectos seleccionados"

# Initiative Admin Form
class InitiativeAdmin(LeafletGeoAdmin):
  model = models.Initiative
  ordering = ('name',)
  list_display = ('name', 'creation_date', 'city', 'topic', 'space', 'agent', 'featured')
  list_filter  = ('featured', 'topic', 'space', 'agent', 'city')
  actions      = [unfeature, feature]

  def get_action_choices(self, request):
    """
    Override blank action string
    @see https://stackoverflow.com/questions/35503403/how-to-remove-in-django-admin-action
    """
    return super(InitiativeAdmin, self).get_action_choices(request, [("", "Elige una acción")])

# Initiative Admin Form
class EventAdmin(LeafletGeoAdmin):
  model = models.Event
  ordering = ('date',)
  list_display = ('title', 'initiative', 'city', 'topic', 'category', 'agent', 'featured')
  list_filter  = ('featured', 'topic', 'category', 'agent')
  actions      = [unfeature, feature]

  def get_action_choices(self, request):
    """
    Override blank action string
    @see https://stackoverflow.com/questions/35503403/how-to-remove-in-django-admin-action
    """
    return super(EventAdmin, self).get_action_choices(request, [("", "Elige una acción")])

# Initiative Admin Form
class CityAdmin(LeafletGeoAdmin):
  model = models.City
  ordering = ('country', 'name')
  list_display = ('name_id', 'country', 'initiatives')

  def name_id(self, obj):
      return "%s [%s]" % (obj.name, obj.id)

  def initiatives(self, obj):
      return models.Initiative.objects.filter(city=obj).count()

  def get_action_choices(self, request):
    """
    Override blank action string
    @see https://stackoverflow.com/questions/35503403/how-to-remove-in-django-admin-action
    """
    return super(CityAdmin, self).get_action_choices(request, [("", "Elige una acción")])


# Register models in admin
admin.site.register(models.City, CityAdmin)
admin.site.register(models.Initiative, InitiativeAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.ODS)
admin.site.register(models.Resource)
