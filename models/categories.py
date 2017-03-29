from django.utils.translation import ugettext_lazy as _

"""
The different categories used by the Models of Civics
"""

TOPICS = (
    ('DC', _('Desarrollo comunitario'),
    ('AU', _('Arte urbano'),
    ('CL', _('Cultura libre'),
    ('DS', _('Deporte / Salud / Cuidados'),
    ('ID', _('Igualdad / Derechos / Memoria'),
    ('EC', _('Ecología / Consumo'),
    ('OE', _('Otras economías'),
    ('EE', _('Educación expandida'),
    ('CT', _('Ciencia / Tecnología'),
    ('MS', _('Movilidad sostenible'),
    ('PG', _('Política y gobernanza'),
    ('UP', _('Urbanismo / Patrimonio'),
)

SPACES = (
    ('CC', _('Centro cultural/comunitario'),
    ('EI', _('Efímero e itinerante'),
    ('IT', _('Intercambio / Trueque'),
    ('DI', _('Digital'),
    ('EA', _('Encuentros / Acciones'),
    ('EP', _('Escuelas populares'),
    ('HU', _('Huerto urbano/rural'),
    ('IU', _('Intervenciones urbanas'),
    ('MC', _('Medios comunitarios de comunicación'),
    ('MS', _('Mercado social / Comercios'),
    ('SE', _('Solares / Espacios recuperados'),
    ('EM', _('Espacios colaborativos/maker'),
)

ACTIVITIES = (
    ('AU', _('Audiovisual'),
    ('CU', _('Curso / Convocatoria'),
    ('DI', _('Digital'),
    ('EN', _('Encuentro'),
    ('EV', _('Evento'),
    ('EX', _('Exposicion'),
    ('FI', _('Fiesta / Concierto'),
    ('PU', _('Publicación'),
    ('TA', _('Taller'),
)

ACTORS = (
    ('IM', _('Iniciativas municipales / Gobierno'),
    ('IC', _('Iniciativa ciudadana'),
    ('OI', _('Organismos internacionales'),
    ('ES', _('Empresa social / Startup'),
    ('UO', _('Universidades / ONG'),
    ('JA', _('Juntas / Asociaciones de vecinos'),
    ('CC', _('Conquistas ciudadanas del pasado'),
)
