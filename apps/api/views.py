from django.shortcuts import render
from apps.models.models import Initiative, City, Event
from apps.models.categories import *
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_protect
import json
from django.utils.text import slugify
from datetime import date
from django.conf import settings
import math

#
#  API
#

no_results = _("No se han encontrado resultados que cumplan con todas las condiciones de filtrado.")

def initiatives_service(request):
    cities = City.objects.annotate(num_refs=Count('initiative')).filter(num_refs__gt=10)
    initiatives = Initiative.objects.filter(city__in=cities)

    if len(initiatives) > 0:
        initiatives_json = {}
        for initiative_json in initiatives:
            coords        = initiative_json.position['coordinates']
            cityname      = initiative_json.city.name if initiative_json.city else 'none'
            countryname   = initiative_json.city.get_country_display() if initiative_json.city else 'none'
            if countryname not in initiatives_json:
                initiatives_json[countryname] = {}
            if cityname not in initiatives_json[countryname]:
                initiatives_json[countryname][cityname] = {}
            city_coords = initiative_json.city.position['coordinates']
            initiatives_json[countryname][cityname]['coordinates'] = [ city_coords[1], city_coords[0] ];
            if 'items' not in initiatives_json[countryname][cityname]:
                initiatives_json[countryname][cityname]['items'] = [];
            initiatives_json[countryname][cityname]['items'].append({
                'id'  : initiative_json.pk,
                'lng' : coords[0],
                'lat' : coords[1],
                'img' : initiative_json.image_medium.url if initiative_json.image else None,
                'cit' : initiative_json.city.name if initiative_json.city else 'none',
                'top' : initiative_json.topic.lower(),
                'age' : initiative_json.agent.lower(),
                'spa' : initiative_json.space.lower(),
            })

        return HttpResponse(json.dumps(initiatives_json), content_type="application/json")

    return HttpResponse(no_results)

def events_service(request):
    cities     = City.objects.annotate(num_refs=Count('initiative')).filter(num_refs__gt=0)
    events     = Event.objects.filter(city__in=cities)

    if len(events) > 0:
        events_json = {}
        for event in events:
            coords        = event.position['coordinates']
            cityname      = event.city.name if event.city else 'none'
            countryname   = event.city.get_country_display() if event.city else 'none'
            if countryname not in events_json:
                events_json[countryname] = {}
            if cityname not in events_json[countryname]:
                events_json[countryname][cityname] = {}
            city_coords = event.city.position['coordinates']
            events_json[countryname][cityname]['coordinates'] = [ city_coords[1], city_coords[0] ];
            if 'items' not in events_json[countryname][cityname]:
                events_json[countryname][cityname]['items'] = [];
            events_json[countryname][cityname]['items'].append({
                'id'    : event.id,
                'lng'   : coords[0],
                'lat'   : coords[1],
                'dat'   : str(event.date),
                'top'   : event.topic.lower(),
                'act'   : event.category.lower(),
                'age'   : event.agent.lower(),
            })

        return HttpResponse(json.dumps(events_json), content_type="application/json")

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

def autocomplete_service(request):
    """ Returns initiatives with names beginning with the query characters. """
    name = request.GET.get('n')
    if(len(name) < 4):
        raise Exception("Queries must be longer than three characters")
    print(name)
    initiatives = Initiative.objects.filter(slug__startswith=slugify(name))
    initiatives_json = []
    # TODO: map this!
    for initiative in initiatives:
        initiatives_json.append({
            'id'  : initiative.pk,
            'nam' : initiative.name,
        })
    return HttpResponse(json.dumps(initiatives_json), content_type="application/json")

def initiative_service(request):
    id = request.GET.get('id')
    initiative    = Initiative.objects.filter(pk=id).first()
    coords        = initiative.position['coordinates']
    cityname      = initiative.city.name if initiative.city else 'none'
    countryname   = initiative.city.get_country_display() if initiative.city else 'none'
    initiative_json = {
        'id'  : initiative.pk,
        'nam' : initiative.name,
        'slu' : initiative.slug,
        'add' : initiative.address,
        'cou' : countryname,
        'lng' : coords[0],
        'lat' : coords[1],
        'des' : initiative.description,
        'img' : initiative.image.url if initiative.image else None,
        'web' : initiative.website,
        'ema' : initiative.email,
        'twi' : initiative.twitter,
        'fac' : initiative.facebook,
        'cities' : cityname,
        'topics' : initiative.topic.lower(),
        'agents' : initiative.agent.lower(),
        'spaces' : initiative.space.lower(),
    }
    return HttpResponse(json.dumps(initiative_json), content_type="application/json")

def event_service(request):
    id = request.GET.get('id')
    event         = Event.objects.filter(pk=id).first()
    coords        = event.position['coordinates']
    cityname      = event.city.name if event.city else 'none'
    countryname   = event.city.get_country_display() if event.city else 'none'
    event = {
        'id'    : event.pk,
        'nam'   : event.title,
        'slu'   : event.slug,
        'img'   : event.image.url if event.image else None,
        'add'   : event.address,
        'dat'   : event.date.strftime("%d/%b/%Y"),
        'tim'   : event.time.strftime("%H:%M"),
        'cou'   : countryname,
        'lng'   : coords[0],
        'lat'   : coords[1],
        'des'   : event.description,
        'ini'   : event.initiative.name,
        'web'   : event.initiative.website,
        'ema'   : event.initiative.email,
        'i_add' : event.initiative.address + ", " + cityname + "(" + countryname + ")",
        'cities'     : cityname,
        'topics'     : event.topic.lower(),
        'agents'     : event.agent.lower(),
        'activities' : event.category.lower(),
    }
    return HttpResponse(json.dumps(event), content_type="application/json")

def initiatives_featured_service(request):
    initiatives_json = {}
    initiatives_json['featured'] = []
    initiatives_featured = Initiative.objects.filter(featured=True)[:9]
    for initiative in initiatives_featured:
        initiatives_json['featured'].append({
            'nam'    : initiative.name,
            'id'     : initiative.id,
            'img'    : initiative.image_medium.url if initiative.image else None,
            'cities' : initiative.city.name if initiative.city else 'none',
        })
    initiatives_json['last'] = []
    initiatives_last = Initiative.objects.order_by('creation_date')[:9]
    for initiative in initiatives_last:
        initiatives_json['last'].append({
            'nam'    : initiative.name,
            'id'     : initiative.id,
            'img'    : initiative.image_medium.url if initiative.image else None,
            'cities' : initiative.city.name if initiative.city else 'none'
        })

    return HttpResponse(json.dumps(initiatives_json), content_type="application/json")

def events_featured_service(request):
    events_json = {}
    events_json['featured'] = []
    events_featured = Event.objects.filter(featured=True).order_by('-date')[:3]
    for event in events_featured:
        events_json['featured'].append({
            'nam'    : event.title,
            'id'     : event.id,
            'img'    : event.image_medium.url if event.image else None,
            'day'    : event.date.strftime('%d'),
            'month'  : event.date.strftime('%b'),
            'cities' : event.city.name if event.city else 'none'
        })
    events_json['last'] = []
    events_last = Event.objects.filter(date__gte=date.today()).order_by('date')[:3]
    for event in events_last:
        events_json['last'].append({
            'nam'    : event.title,
            'id'     : event.id,
            'img'    : event.image_medium.url if event.image else None,
            'day'    : event.date.strftime('%d'),
            'month'  : event.date.strftime('%b'),
            'cities' : event.city.name if event.city else 'none'
        })

    return HttpResponse(json.dumps(events_json), content_type="application/json")

@csrf_protect
def create_event(request):
    """
    Create an event in database.
    To be triggered by ajax calls from static/js/facebook.js

    """

    if request.method == 'POST':
        if request.is_ajax:
            initiative_id = request.POST.get('initiative_id')
            initiative = Initiative.objects.filter(pk=initiative_id).first()
            e = Event.objects.create(
                title       = request.POST.get('name'),
                description = request.POST.get('description'),
                date        = request.POST.get('formatted_date'),
                time        = request.POST.get('time'),
                position    = json.loads('{ "type": "Point", "coordinates": [' + request.POST.get('lon') + ',' + request.POST.get('lat') +'] }'),
                facebook_id = request.POST.get('facebook_id'),
                initiative  = initiative,
                address     = request.POST.get('address'),
                topic       = initiative.topic,
                agent       = initiative.agent,
                city        = initiative.city,
                category    = request.POST.get('category'),
            )
            return HttpResponse(e.id, content_type="application/json")
    else:
        return HttpResponse("Prohibido", content_type="application/json")

def events_by_fb_id_service(request):
    """
    Get Facebook id's of events in database.

    """

    events = Event.objects.filter(facebook_id__isnull=False)
    events_json = []
    for event in events:
        events_json.append(event.facebook_id)
    return HttpResponse(json.dumps(events_json), content_type="application/json")
