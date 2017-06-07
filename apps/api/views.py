from django.shortcuts import render
from apps.models.models import Initiative, City, Event
from apps.models.categories import *
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.db.models import Count
import json
from django.utils.text import slugify
from datetime import date
import pycountry
from django.conf import settings

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
                'lat'          : coords[1],
                'lng'          : coords[0],
                'id'           : event_json.id,
                'title'        : event_json.title,
                'img'          : event_json.image_medium.url if event_json.image_medium else '',
                'description'  : event_json.description,
                'topic'        : event_json.topic.lower(),
                'activity'     : event_json.category.lower(),
                'agent'        : event_json.agent.lower(),
                'city'         : event_json.city.name,
                'country'      : event_json.city.get_country_display(),
                'date'         : event_json.date.strftime('%d %B %Y'),
                'time'         : str(event_json.time),
                'address'      : event_json.address if event_json.address else '',
                'initiative'   : event_json.initiative.name,
                'init_website' : event_json.initiative.website,
                'init_email'   : event_json.initiative.email,
                'init_address' : event_json.initiative.address,
            }
            events_json.append(event_json)

        return HttpResponse(json.dumps(events_json, indent=4), content_type="application/json")

    return HttpResponse(no_results)


def initiatives_service_xls(request):
    import xlwt

    topics = request.GET.get('topics').split(',')[0:-1];
    spaces = request.GET.get('spaces').split(',')[0:-1];
    agents = request.GET.get('agents').split(',')[0:-1];

    initiatives = Initiative.objects.all()
    if len(topics) > 0:
        initiatives = initiatives.filter(topic__in=topics)
    if len(spaces) > 0:
        initiatives = initiatives.filter(space__in=spaces)
    if len(agents) > 0:
        initiatives = initiatives.filter(agent__in=agents)

    response = HttpResponse(content_type='application/ms-excel')
    filename = 'iniciativas-civics__' + date.today().isoformat() + '.xls'
    response['Content-Disposition'] = 'attachment; filename=' + filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Initiatives")
    ezxf = xlwt.easyxf

    # Write headers
    count_style = ezxf('font: bold on, name monospace, height 320')
    ws.write(0, 0, "CIVICS.CC # " + date.today().strftime("%d/%m/%Y"), count_style)
    count_style = ezxf('font: bold off, name monospace, height 240')
    count = str(initiatives.count()) + " iniciativas encontradas en las categorías: "
    topics_keys = dict(TOPICS)
    spaces_keys = dict(SPACES)
    agents_keys = dict(AGENTS)
    for topic in topics:
        if topic:
            count += str(topics_keys[topic]) + " · "
    for space in spaces:
        if space:
            count += str(spaces_keys[space]) + " · "
    for agent in agents:
        if agent:
            count += str(agents_keys[agent]) + " · "

    ws.write(1, 0, count, count_style)
    ws.row(0).height_mismatch = True
    ws.row(1).height_mismatch = True
    ws.row(0).height = 368
    ws.row(1).height = 368

    row_num = 4
    columns = [
        (u"Nombre de la iniciativa", 12000),
        (u"Descripción", 25600),
        (u"Temática", 12000),
        (u"Espacio", 12000),
        (u"Agente", 12000),
        (u"Facebook", 12000),
        (u"Twitter", 12000),
        (u"Web", 12000),
        (u"Ciudad", 8000),
        (u"País", 8000),
        (u"Latitud", 4000),
        (u"Longitud", 4000),
        (u"Fecha de creación", 6000),
    ]

    xlwt.add_palette_colour("header_background", 0x21)
    wb.set_colour_RGB(0x21, 50, 50, 50)
    headers_style = ezxf('font: bold on, color white, name monospace, height 200; align: wrap on, horz center, vert center; borders: bottom thin, top thin; pattern: pattern solid, fore_colour header_background')

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], headers_style)
        ws.col(col_num).width = columns[col_num][1]
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 368

    firstcol_style = ezxf('font: height 200, name monospace, bold on; align: wrap on, vert center, horiz center')
    cell_style = ezxf('font: height 200, name monospace, bold off; align: wrap on, vert center, horiz center')
    for initiative in initiatives:
        row_num += 1
        row = [
            initiative.name,
            initiative.description.strip(),
            initiative.get_topic_display(),
            initiative.get_space_display(),
            initiative.get_agent_display(),
            initiative.facebook,
            initiative.twitter,
            initiative.website,
            initiative.city.name if initiative.city else "None",
            initiative.city.get_country_display() if initiative.city else "None",
            initiative.position['coordinates'][0],
            initiative.position['coordinates'][1],
            initiative.creation_date.strftime("%d/%m/%Y"),
        ]
        # Initiative name
        ws.write(row_num, 0, row[0], firstcol_style)
        for col_num in range(1, len(row)):
            content = row[col_num]
            ws.write(row_num, col_num, row[col_num], cell_style)

        content_length = len( initiative.description )
        characters_per_line = 100
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = max(math.ceil(content_length/characters_per_line * 480), 480)

    wb.save(response)
    return response

def events_service_xls(request):
    import xlwt

    topics     = request.GET.get('topics').split(',')[0:-1];
    activities = request.GET.get('activities').split(',')[0:-1];
    agents     = request.GET.get('agents').split(',')[0:-1];

    events = Event.objects.all()
    if len(topics) > 0:
        events = events.filter(topic__in=topics)
    if len(activities) > 0:
        events = events.filter(activity__in=activities)
    if len(agents) > 0:
        events = events.filter(agent__in=agents)

    response = HttpResponse(content_type='application/ms-excel')
    filename = 'eventos-civics__' + date.today().isoformat() + '.xls'
    response['Content-Disposition'] = 'attachment; filename=' + filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Initiatives")
    ezxf = xlwt.easyxf

    # Write headers
    count_style = ezxf('font: bold on, name monospace, height 320')
    ws.write(0, 0, "CIVICS.CC # " + date.today().strftime("%d/%m/%Y"), count_style)
    count_style = ezxf('font: bold off, name monospace, height 240')
    count = str(events.count()) + " eventos encontrados en las categorías: "
    topics_keys = dict(TOPICS)
    activities_keys = dict(ACTIVITIES)
    agents_keys = dict(AGENTS)
    for topic in topics:
        if topic:
            count += str(topics_keys[topic]) + " · "
    for activity in activities:
        if activity:
            count += str(activities_keys[activity]) + " · "
    for agent in agents:
        if agent:
            count += str(agents_keys[agent]) + " · "

    ws.write(1, 0, count, count_style)
    ws.row(0).height_mismatch = True
    ws.row(1).height_mismatch = True
    ws.row(0).height = 368
    ws.row(1).height = 368

    row_num = 4
    columns = [
        (u"Título", 12000),
        (u"Resumen", 25600),
        (u"Temática", 12000),
        (u"Actividad", 12000),
        (u"Agente", 12000),
        (u"Latitud", 4000),
        (u"Longitud", 4000),
        (u"Fecha de creación", 6000),
    ]

    xlwt.add_palette_colour("header_background", 0x21)
    wb.set_colour_RGB(0x21, 50, 50, 50)
    headers_style = ezxf('font: bold on, color white, name monospace, height 200; align: wrap on, horz center, vert center; borders: bottom thin, top thin; pattern: pattern solid, fore_colour header_background')

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], headers_style)
        ws.col(col_num).width = columns[col_num][1]
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 368

    firstcol_style = ezxf('font: height 200, name monospace, bold on; align: wrap on, vert center, horiz center')
    cell_style = ezxf('font: height 200, name monospace, bold off; align: wrap on, vert center, horiz center')
    for event in events:
        row_num += 1
        row = [
            event.title,
            event.description.strip(),
            event.get_topic_display(),
            event.get_category_display(),
            event.get_agent_display(),
            event.position['coordinates'][0],
            event.position['coordinates'][1],
            event.creation_date.strftime("%d/%m/%Y"),
        ]
        # Initiative name
        ws.write(row_num, 0, row[0], firstcol_style)
        for col_num in range(1, len(row)):
            content = row[col_num]
            ws.write(row_num, col_num, row[col_num], cell_style)

        content_length = len( event.description )
        characters_per_line = 100
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = max(math.ceil(content_length/characters_per_line * 480), 480)

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
    countries_data = open( settings.STATIC_ROOT + '/civics/geojson/countries-medium--simplified.json' )
    return HttpResponse(countries_data, content_type="application/json")
