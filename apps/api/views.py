# python
import json
import math
from datetime import date
# django
from django.conf import settings
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_protect
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import Q
# project
from apps.models.categories import *
from apps.models.models import Initiative, City, Event
from .serializers import CivicsJSONSerializer
from apps.models.forms import EventForm

#
#  API
#

no_results = _("No se han encontrado resultados que cumplan con todas las condiciones de filtrado.")

def initiatives_service(request):
    cities = City.objects.annotate(num_refs=Count('initiative')).filter(num_refs__gt=10)
    initiatives = Initiative.objects.filter(city__in=cities).select_related()
    return JsonResponse(CivicsJSONSerializer().serialize(initiatives, fields=('name', 'position', 'image', 'city', 'topic', 'agent', 'space')), safe=False)

def events_service(request):
    cities = City.objects.annotate(num_initiatives=Count('initiative')).filter(num_initiatives__gt=10)
    events = Event.objects.filter(city__in=cities).select_related()
    return JsonResponse(CivicsJSONSerializer().serialize(events, fields=('title', 'position', 'image', 'thumbnail', 'image', 'city', 'topic', 'agent', 'category', 'date', 'expiration')), safe=False)

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
    if request.user.is_staff:
        columns.append( (u"Email", 12000) )

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
        if request.user.is_staff:
            row.append( initiative.email )
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
        (u"Iniciativa promotora", 12000),
        (u"Fecha", 6000),
        (u"Resumen", 25600),
        (u"Temática", 12000),
        (u"Actividad", 12000),
        (u"Agente", 12000),
        (u"Ciudad", 6000),
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
            event.initiative.name,
            event.date.strftime("%d/%m/%Y"),
            event.description.strip(),
            event.get_topic_display(),
            event.get_category_display(),
            event.get_agent_display(),
            event.city.name,
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
    if(len(name) < 3):
        raise Exception("Queries must be longer than two characters")
    initiatives = Initiative.objects.filter(slug__contains=slugify(name))
    initiatives_json = []
    # TODO: map this!
    for initiative in initiatives:
        q        = name.upper()
        new_name = initiative.name.upper().replace(q, "<i>" + q + "</i>")
        initiatives_json.append({
            'id'  : initiative.pk,
            'nam' : new_name,
        })
    return HttpResponse(json.dumps(initiatives_json), content_type="application/json")

def media(url):
    uri     = url.split('://')[1]
    service = uri.split('/')[0]
    if service == 'vimeo.com':
        return 'https://player.vimeo.com/video/' + uri.split('/')[1]
    elif service == 'youtube.com':
        return 'https://www.youtube.com/embed/' + uri.split('?v=')[1]

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
        'vid' : media(initiative.video) if initiative.video else '',
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
        'vid'   : event.video,
        'add'   : event.address,
        'dat'   : event.date.strftime("%d/%b/%Y"),
        'tim'   : event.time.strftime("%H:%M"),
        'cou'   : countryname,
        'lng'   : coords[0],
        'lat'   : coords[1],
        'vid'   : media(event.video) if event.video else '',
        'des'   : event.description,
        'ewe'   : event.website,
        'per'   : event.periodicity if event.periodicity else '',
        'exp'   : event.expiration.strftime("%d/%b/%Y") if event.expiration else '',
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
    initiatives_featured = Initiative.objects.filter(featured=True)[:8]
    for initiative in initiatives_featured:
        initiatives_json['featured'].append({
            'nam'    : initiative.name,
            'id'     : initiative.id,
            'img'    : initiative.image_medium.url if initiative.image else None,
            'cities' : initiative.city.name if initiative.city else 'none',
        })
    initiatives_json['last'] = []
    initiatives_last = Initiative.objects.order_by('-creation_date')[:8]
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
    events_featured = Event.objects.filter(featured=True).order_by('-date')[:8]
    for event in events_featured:
        events_json['featured'].append({
            'nam'        : event.title,
            'id'         : event.id,
            'img'        : event.image_medium.url if event.image else None,
            'date'       : str(event.date),
            'expiration' : str(event.expiration) if event.expiration else None,
            'cities'     : event.city.name if event.city else 'none'
        })
    events_json['last'] = []
    events_last = Event.objects.filter(date__gte=date.today()).order_by('date')[:8]
    for event in events_last:
        events_json['last'].append({
            'nam'        : event.title,
            'id'         : event.id,
            'img'        : event.image_medium.url if event.image else None,
            'date'       : str(event.date),
            'expiration' : str(event.expiration) if event.expiration else None,
            'cities'     : event.city.name if event.city else 'none'
        })

    return HttpResponse(json.dumps(events_json), content_type="application/json")

@csrf_protect
def create_event(request):
    """
    Create an event in database.
    To be triggered by ajax calls from static/js/facebook.js
    """

    if request.method == 'POST' and request.is_ajax:
        e = {}
        req = request.POST
        initiative_id      = int(req.get('initiative'))
        initiative         = Initiative.objects.get(pk=initiative_id)
        lat                = req.get('lat') if req.get('lat') else initiative.position['coordinates'][0]
        lon                = req.get('lon') if req.get('lon') else initiative.position['coordinates'][1]
        e['title']         = req.get('name')
        e['description']   = req.get('description')
        e['initiative']    = initiative.id
        e['date']          = req.get('date') if req.get('date') else date.today().strftime("%d/%m/%Y")
        e['time']          = req.get('time') if req.get('time') else '12:00'
        e['address']       = req.get('address') if req.get('address') else initiative.address,
        e['topic']         = initiative.topic
        e['agent']         = initiative.agent
        e['city']          = initiative.city.id
        e['position']      = json.loads('{ "type": "Point", "coordinates": ['+ str(lat) +','+ str(lon) +'] }')
        e['category']      = req.get('category')
        e['facebook_id']   = req.get('facebook_id') if req.get('facebook_id') else None
        e['google_id']     = req.get('google_id') if req.get('google_id') else None
        print(e)
        form = EventForm(e)
        if form.is_valid():
            new_event = form.save()
            return HttpResponse(new_event.id, content_type="application/json")
        else:
            print("El formulario no es valido:")
            print(form.errors)
            return HttpResponse("There were some problems uploading the event. Check form data.", content_type="application/json")

    else:
        return HttpResponse("This action is forbidden.", content_type="application/json")


def events_by_fb_id_service(request):
    """
    Get social netowrk id's of events in database.
    """

    events = Event.objects.filter( Q(google_id__isnull=False) | Q(facebook_id__isnull=False) )
    events_json = []
    for event in events:
        if event.facebook_id:
            events_json.append(event.facebook_id)
        if event.google_id:
            events_json.append(event.google_id)
    return HttpResponse(json.dumps(events_json), content_type="application/json")


def cities_with_initiatives(request):
    """
    Get cities related to initiatives
    """

    cities = City.objects.annotate(num_refs=Count('initiative')).filter(num_refs__gt=10)
    response = {}
    for city in cities:
        response[city.pk] = { 'name' : city.name, 'id' : city.pk, 'country' : city.country.name, 'coordinates' : city.position['coordinates'] }
    return HttpResponse( json.dumps(response), content_type="application/json" );


def cities_with_events(request):
    """
    Get cities related to events
    """

    cities = City.objects.annotate(num_initiatives=Count('initiative'), num_events=Count('event')).filter(num_initiatives__gt=10, num_events__gt=1)
    response = {}
    for city in cities:
        response[city.pk] = { 'name' : city.name, 'id' : city.pk, 'country' : city.country.name, 'coordinates' : city.position['coordinates'] }
    return HttpResponse( json.dumps(response), content_type="application/json" );
