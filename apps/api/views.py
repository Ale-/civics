from django.shortcuts import render
from apps.models.models import Initiative, City, Event
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.db.models import Count
import json
from django.utils.text import slugify
from datetime import date
import pycountry
from django.contrib.staticfiles.templatetags.staticfiles import static

#
#  API
#

no_results = _("No se han encontrado resultados que cumplan con todas las condiciones de filtrado.")

def initiatives_service(request):
    city   = request.GET.get('city');
    topics = request.GET.get('topics').split(',');
    spaces = request.GET.get('spaces').split(',');
    agents = request.GET.get('agents').split(',');
    cities = City.objects.annotate(num_refs=Count('initiative')).filter(num_refs__gt=10)
    initiatives = Initiative.objects.filter(city__in=cities)
    if city   != 'all':
        initiatives = initiatives.filter(city=city);
    if topics != ['all']:
        initiatives = initiatives.filter(topic__in=topics)
    if spaces != ['all']:
        initiatives = initiatives.filter(space__in=spaces)
    if agents != ['all']:
        initiatives = initiatives.filter(topic__in=agents)
    if len(initiatives) > 0:
        initiatives_json = []
        for initiative_json in initiatives:
            coords        = initiative_json.position['coordinates']
            cityname      = initiative_json.city.name if initiative_json.city else 'none'
            countryname   = initiative_json.city.country if initiative_json.city else 'none'
            initiative_json = {
                'lng'            : coords[0],
                'lat'            : coords[1],
                'city'           : cityname,
                'country'        : countryname,
                'name'           : initiative_json.name,
                'slug'           : initiative_json.slug,
                'img'            : initiative_json.image.url if initiative_json.image else '',
                'id'             : initiative_json.pk,
                'description'    : initiative_json.description,
                'topic'          : initiative_json.topic.lower(),
                'agent'          : initiative_json.agent.lower(),
                'space'          : initiative_json.space.lower(),
                'website'        : initiative_json.website,
                'email'          : initiative_json.email,
                'address'        : initiative_json.address,
                'layer'          : cityname,
            }
            initiatives_json.append(initiative_json)

        return HttpResponse(json.dumps(initiatives_json, indent=4), content_type="application/json")

    return HttpResponse(no_results)


def events_service(request):
    city       = request.GET.get('city');
    topics     = request.GET.get('topics').split(',');
    categories = request.GET.get('categories').split(',');
    agents     = request.GET.get('agents').split(',');
    cities     = City.objects.annotate(num_refs=Count('initiative')).filter(num_refs__gt=10)
    events     = Event.objects.filter(city__in=cities)
    if city   != 'all':
        events = events.filter(city=city);
    if topics != ['all']:
        events = events.filter(topic__in=topics)
    if categories != ['all']:
        events = events.filter(category__in=categories)
    if agents != ['all']:
        events = events.filter(topic__in=agents)
    if len(events) > 0:
        events_json = []
        for event_json in events:
            coords        = event_json.position['coordinates']
            cityname      = event_json.city.name if event_json.city else 'none'
            event_json = {
                'lat'            : coords[0],
                'lng'            : coords[1 ],
                'title'          : event_json.title,
                'description'    : event_json.description,
                'topic'          : event_json.topic,
                'category'       : event_json.category,
                'agent'          : event_json.agent,
            }
            events_json.append(event_json)

        return HttpResponse(json.dumps(events_json, indent=4), content_type="application/json")

    return HttpResponse(no_results)


def initiatives_service_xls(request):
    import xlwt

    topics = request.GET.get('topics').split(',');
    spaces = request.GET.get('spaces').split(',');
    agents = request.GET.get('agents').split(',');

    initiatives = Initiative.objects.filter(topic__in=topics, space__in=spaces, agent__in=agents)

    response = HttpResponse(content_type='application/ms-excel')
    filename = 'iniciativas-civics__' + date.today().isoformat() + '.xls'
    response['Content-Disposition'] = 'attachment; filename=' + filename
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Initiatives")

    row_num = 0

    columns = [
        (u"Nombre de la iniciativa", 12000),
        (u"Descripción", 24000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for initiative in initiatives:
        print(initiative)
        row_num += 1
        row = [
            initiative.name,
            initiative.description,
        ]
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def cities_service(request):
    cities = City.objects.annotate(num_refs=Count('initiative')).filter(num_refs__gt=10)
    if len(cities) > 0:
        cities_json = {}
        for city in cities:
            coords  = city.position['coordinates']
            country = pycountry.countries.get(alpha_2=city.country).name
            if(country in cities_json):
                cities_json[country].append( city.name )
            else:
                cities_json[country] = [ city.name ]
        return HttpResponse(json.dumps(cities_json, indent=4), content_type="application/json")

    return HttpResponse(no_results)

def countries_service(request):
    # TODO: catch exceptions
    countries_data = open( 'static/civics/geojson/countries-medium--simplified.json' )
    return HttpResponse(countries_data, content_type="application/json")
