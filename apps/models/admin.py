# Dependencies
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

# Current models
from . import models

# Register models in admin
admin.site.register(models.City, LeafletGeoAdmin)
admin.site.register(models.Initiative, LeafletGeoAdmin)
admin.site.register(models.Event, LeafletGeoAdmin)
