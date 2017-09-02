'use strict';

/**
 *  i18n
 *  A service to handle interface translation
 */
angular.module('civics.i18n', [])

.filter('t', function(Langs) {
    return function(text){
        return Langs.get(text);
    };
})

.factory('Langs', function()
{
    var interfaz = {
        pt: {
            //views/content-list.html
            'Mostrando' : 'Mostrando',
            'de' : 'de',
            'elementos filtrados' : 'elementos filtrados',
            'Ver página anterior' : 'Ver página anterior',
            'Ver página siguiente' : 'Ver página siguiente',
            'Parece que todavía no se han generado contenidos de este tipo' : 'Parece que todavía no se han generado contenidos de este tipo',
            //views/content-featured.html
            'Volver atrás' : 'Volver atrás',
            'Iniciativas ciudadanas destacadas' : 'Iniciativas ciudadanas destacadas',
            'Actividades ciudadanas destacadas' : 'Actividades ciudadanas destacadas',
            'Últimas iniciativas ciudadanas incorporadas' : 'Últimas iniciativas ciudadanas incorporadas',
            'Próximas actividades ciudadanas' : 'Próximas actividades ciudadanas',
            //directives/map-actions.html
            'Usa la leyenda para filtrar los contenidos según tus intereses.' : 'Usa la leyenda para filtrar los contenidos según tus intereses.',
            'Ver las iniciativas en formato mapa' : 'Ver las iniciativas en formato mapa',
            'Ver las iniciativas en formato lista' : 'Ver las iniciativas en formato lista',
            'Ver las iniciativas destacadas' : 'Ver las iniciativas destacadas',
            'Ver los eventos en formato mapa' : 'Ver los eventos en formato mapa',
            'Ver los eventos en formato lista' : 'Ver los eventos en formato lista',
            'Ver los eventos destacados' : 'Ver los eventos destacados',
            'Descargar la vista en XLS' : 'Descargar la vista en XLS',
            'Mostrando' : 'Mostrando',
            'iniciativas' : 'iniciativas',
            'eventos' : 'eventos',
            'Eliminar filtros' : 'Eliminar filtros',
            //directives/map-filters.html
            'Ciudad' : 'Cidade',
            'Temática' : 'Temática',
            'Espacio' : 'Espaço',
            'Actividad' : 'Atividade',
            'Agente' : 'Agente',
            //directives/search.html
            'Busca por nombre' : 'Busca por nombre',
            //directives/social-widget.html
            'Perfil de Civics en Facebook' : 'Perfil de Civics en Facebook',
            'Perfil de Civics en Twitter' : 'Perfil de Civics en Twitter',
            'Repositorio de Civics en Github' : 'Repositorio de Civics en Github',
            'Contacta con Civics' : 'Contacta con Civics',
            //directives/time-filter.html
            'Todas' : 'Todas',
            'Hoy' : 'Hoy',
            'Mañana' : 'Mañana',
            'Próximos 7 días' : 'Próximos 7 días',
            'Próximos 30 días' : 'Próximos 30 días',
            'Pasadas' : 'Pasadas',
            'Filtra por fecha' : 'Filtra por fecha',
            //services/Categories.js
            'Desarrollo comunitario' : 'Desarrollo comunitario',
            'Arte urbano' : 'Arte urbano',
            'Cultura libre' : 'Cultura libre',
            'Deporte / Salud / Cuidados' : 'Deporte / Salud / Cuidados',
            'Igualdad / Derechos / Memoria' : 'Igualdad / Derechos / Memoria',
            'Ecología / Consumo' : 'Ecología / Consumo',
            'Otras economías' : 'Otras economías',
            'Educación expandida' : 'Educación expandida',
            'Ciencia / Tecnología' : 'Ciencia / Tecnología',
            'Movilidad sostenible' : 'Movilidad sostenible',
            'Política y gobernanza' : 'Política y gobernanza',
            'Urbanismo / Patrimonio' : 'Urbanismo / Patrimonio',
            'Periodismo comunitario' : 'Periodismo comunitario',
            'Centro cultural / comunitario' : 'Centro cultural / comunitario',
            'Efímero e itinerante' : 'Efímero e itinerante',
            'Intercambio / Trueque' : 'Intercambio / Trueque',
            'Digital' : 'Digital',
            'Encuentros / Acciones' : 'Encuentros / Acciones',
            'Escuelas populares' : 'Escuelas populares',
            'Huerto urbano / rural' : 'Huerto urbano / rural',
            'Intervenciones urbanas' : 'Intervenciones urbanas',
            'Medios de comunicación comunitaria' : 'Medios de comunicación comunitaria',
            'Mercado social / Comercios' : 'Mercado social / Comercios',
            'Solares / Espacios recuperados' : 'Solares / Espacios recuperados',
            'Labs / Colaborativos / Maker' : 'Labs / Colaborativos / Maker',
            'Iniciativas municipales / Gobierno' : 'Iniciativas municipales / Gobierno',
            'Universidades / ONG / Fundaciones' : 'Universidades / ONG / Fundaciones',
            'Organismos internacionales' : 'Organismos internacionales',
            'Empresa social / Startup' : 'Empresa social / Startup',
            'Iniciativa ciudadana' : 'Iniciativa ciudadana',
            'Juntas / Asociaciones de vecinos' : 'Juntas / Asociaciones de vecinos',
            'Conquistas ciudadanas del pasado' : 'Conquistas ciudadanas del pasado',
            'Audiovisual' : 'Audiovisual',
            'Curso / Convocatoria' : 'Curso / Convocatoria',
            'Digital' : 'Digital',
            'Encuentro' : 'Encuentro',
            'Evento' : 'Evento',
            'Exposicion' : 'Exposicion',
            'Fiesta / Concierto' : 'Fiesta / Concierto',
            'Publicación' : 'Publicación',
            'Taller' : 'Taller',
        },
    }

    var l = window.location.pathname.split('/')[1];

    return {
        lang : l,

        langs : [
          { k: 'pt', v: 'pt'},
          { k: 'es', v: 'es'},
        ],

        get: function(text){
            var lang = this.lang;
            return (lang == 'es' || !interfaz[lang] ) ? text : interfaz[lang][text];
        }
    }
});
