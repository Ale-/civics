angular.module('civics.categories_service', [])

.factory('Categories', function(){

    this.topics = {
      'dc': 'Desarrollo comunitario',
      'au': 'Arte urbano',
      'cl': 'Cultura libre',
      'ds': 'Deporte / Salud / Cuidados',
      'id': 'Igualdad / Derechos / Memoria',
      'ec': 'Ecología / Consumo',
      'oe': 'Otras economías',
      'ee': 'Educación expandida',
      'ct': 'Ciencia / Tecnología',
      'ms': 'Movilidad sostenible',
      'pg': 'Política y gobernanza',
      'up': 'Urbanismo / Patrimonio',
      'pc': 'Periodismo comunitario',
      'in': 'Infancia',
      'di': 'Digitalización / Datos Abiertos',
      'fe': 'Feminismos',
    };

    this.spaces = {
      'cc': 'Centro cultural / comunitario',
      'ei': 'Efímero e itinerante',
      'it': 'Intercambio / Trueque',
      'di': 'Digital',
      'ea': 'Encuentros / Acciones',
      'ep': 'Escuelas populares',
      'hu': 'Huerto urbano / rural',
      'iu': 'Intervenciones urbanas',
      'mc': 'Medios de comunicación comunitaria',
      'ms': 'Mercado social / Comercios',
      'se': 'Solares / Espacios recuperados',
      'em': 'Labs / Colaborativos / Maker',
    };

    this.agents = {
      'im': 'Iniciativas municipales / Gobierno',
      'uo': 'Universidades / ONG / Fundaciones',
      'oi': 'Organismos internacionales',
      'es': 'Empresa social / Startup',
      'ic': 'Iniciativa ciudadana',
      'ja': 'Juntas / Asociaciones de vecinos',
      'cc': 'Iniciativas ciudadanas inactivas'
    };

    this.activities = {
      'au': 'Audiovisual',
      'cu': 'Curso / Convocatoria',
      'di': 'Digital',
      'en': 'Encuentro',
      'ev': 'Evento',
      'ex': 'Exposicion',
      'fi': 'Fiesta / Concierto',
      'pu': 'Publicación',
      'ta': 'Taller',
    };

    this.ods = {
      '1'  : 'Fin de la pobreza',
      '2'  : 'Hambre cero',
      '3'  : 'Salud y bienestar',
      '4'  : 'Educación de calidad',
      '5'  : 'Igualdad de género',
      '6'  : 'Agua limpia y saneamiento',
      '7'  : 'Energía asequible y no contaminante',
      '8'  : 'Trabajo decente y crecimiento económico',
      '9'  : 'Industria, innovación e infraestructura',
      '10' : 'Reducción de las desigualdades',
      '11' : 'Ciudades y comunidades sostenibles',
      '12' : 'Producción y consumo responsables',
      '13' : 'Acción por el clima',
      '14' : 'Vida submarina',
      '15' : 'Vida de ecosistemas terrestres',
      '16' : 'Paz, justicia e instituciones sólidas',
      '17' : 'Alianzas para lograr los objetivos',
    };

    this.city_initiatives = {};
    this.city_events = {};
    this.cities = {};

    this.addInitiativeCity = function(country, name, id, coords){
        if(!this.city_initiatives[country])
            this.city_initiatives[country] = {}
        if(!this.city_initiatives[country][id]) {
            this.city_initiatives[country][id] = {
                'name'   : name,
                'coords' : [ coords[1], coords[0] ],
            };
            this.cities[id] = name;
        }
    }

    this.addEventCity = function(country, name, id, coords){
        if(!this.city_events[country])
            this.city_events[country] = {}
        if(!this.city_events[country][id]) {
            this.city_events[country][id] = {
                'name'   : name,
                'coords' : [ coords[1], coords[0] ],
            };
            this.cities[id] = name;
        }
    }

    return this;

})
