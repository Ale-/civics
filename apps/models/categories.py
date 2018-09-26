from django.utils.translation import ugettext_lazy as _

"""
The different categories used by the Models of Civics
"""

TOPICS = (
    ('DC', _('Desarrollo comunitario')),
    ('AU', _('Arte urbano')),
    ('CL', _('Cultura libre')),
    ('DS', _('Deporte / Salud / Cuidados')),
    ('ID', _('Igualdad / Derechos / Memoria')),
    ('EC', _('Ecología / Consumo')),
    ('OE', _('Otras economías')),
    ('EE', _('Educación expandida')),
    ('CT', _('Ciencia / Tecnología')),
    ('MS', _('Movilidad sostenible')),
    ('PG', _('Política y gobernanza')),
    ('UP', _('Urbanismo / Patrimonio')),
    ('PC', _('Periodismo comunitario')),
    ('IN', _('Infancia')),
)

SPACES = (
    ('CC', _('Centro cultural / comunitario')),
    ('EI', _('Efímero e itinerante')),
    ('IT', _('Intercambio / Trueque')),
    ('DI', _('Digital')),
    ('EA', _('Encuentros / Acciones')),
    ('EP', _('Escuelas populares')),
    ('HU', _('Huerto urbano/rural')),
    ('IU', _('Intervenciones urbanas')),
    ('MC', _('Medios de comunicación comunitaria')),
    ('MS', _('Mercado social / Comercios')),
    ('SE', _('Solares / Espacios recuperados')),
    ('EM', _('Labs / Colaborativos / Maker')),
)

ACTIVITIES = (
    ('AU', _('Audiovisual')),
    ('CU', _('Curso / Convocatoria')),
    ('DI', _('Digital')),
    ('EN', _('Encuentro')),
    ('EV', _('Evento')),
    ('EX', _('Exposicion')),
    ('FI', _('Fiesta / Concierto')),
    ('PU', _('Publicación')),
    ('TA', _('Taller')),
)

AGENTS = (
    ('IM', _('Iniciativas municipales / Gobierno')),
    ('UO', _('Universidades / ONG / Fundaciones')),
    ('OI', _('Organismos internacionales')),
    ('ES', _('Empresa social / Startup')),
    ('IC', _('Iniciativa ciudadana')),
    ('JA', _('Juntas / Asociaciones de vecinos')),
    ('CC', _('Iniciativas ciudadanas inactivas'))
)

ODS = (
    ('1', _('Fin de la pobreza')),
    ('2', _('Hambre cero')),
    ('3', _('Salud y bienestar')),
    ('4', _('Educación de calidad')),
    ('5', _('Igualdad de género')),
    ('6', _('Agua limpia y saneamiento')),
    ('7', _('Energía asequible y no contaminante')),
    ('8', _('Trabajo decente y crecimiento económico')),
    ('9', _('Industria, innovación e infraestructura')),
    ('10',_('Reducción de las desigualdades')),
    ('11',_('Ciudades y comunidades sostenibles')),
    ('12',_('Producción y consumo responsables')),
    ('13',_('Acción por el clima')),
    ('14',_('Vida submarina')),
    ('15',_('Vida de ecosistemas terrestres')),
    ('16',_('Paz, justicia e instituciones sólidas')),
    ('17',_('Alianzas para lograr los objetivos')),
)
