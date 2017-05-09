from django.shortcuts import render
from apps.models.models import Initiative
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
import json

#
#  API
#

no_results = _("No se han encontrado resultados que cumplan con todas las condiciones de filtrado.")

def initiatives_service(request):
    city   = request.GET.get('city');
    topics = request.GET.get('topics').split(',');
    spaces = request.GET.get('spaces').split(',');
    agents = request.GET.get('agents').split(',');
    initiatives = Initiative.objects.filter(city=city);
    print(initiatives)
    if topics != ['all']:
        initiatives = initiatives.filter(topic__in=topics)
    if spaces != ['all']:
        initiatives = initiatives.filter(space__in=spaces)
    if agents != ['all']:
        initiatives = initiatives.filter(topic__in=agents)
    if len(initiatives) > 0:
        initiatives_json = []
        for initiative_json in initiatives:
            initiative_json = { 'name' : initiative_json.name }
            initiatives_json.append(initiative_json)
        return HttpResponse(json.dumps(initiatives_json, indent=4), content_type="application/json")

    return HttpResponse(no_results)
