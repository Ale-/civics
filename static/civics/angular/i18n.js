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
          'elementos filtrados' : 'itens filtrados',
          'Ver página anterior' : 'Veja a página anterior',
          'Ver página siguiente' : 'Veja a próxima página',
          'Parece que todavía no se han generado contenidos de este tipo' : 'Parece que o conteúdo desse tipo ainda não foi gerado',
          //views/content-featured.html
          'Volver atrás' : 'Voltar atrás',
          'Iniciativas ciudadanas destacadas' : 'Iniciativas cidadãs destacadas',
          'Actividades ciudadanas destacadas' : 'Atividades cidadãs destacadas',
          'Últimas iniciativas ciudadanas incorporadas' : 'Iniciativas incorporadas recentemente',
          'Próximas actividades ciudadanas' : 'Próximas atividades do cidadão',
          //directives/map-actions.html
          'Usa la leyenda para filtrar los contenidos según tus intereses.' : 'Use a legenda para filtrar o conteúdo de acordo com seus interesses.',
          'Ver las iniciativas en formato mapa' : 'Veja as iniciativas em formato de mapa',
          'Ver las iniciativas en formato lista' : 'Veja as iniciativas em formato de lista',
          'Ver las iniciativas destacadas' : 'Veja iniciativas pendentes',
          'Ver los eventos en formato mapa' : 'Veja eventos no formato do mapa',
          'Ver los eventos en formato lista' : 'Visualizar eventos em formato de lista',
          'Ver los eventos destacados' : 'Ver eventos em destaque',
          'Descargar la vista en XLS' : 'Baixe a visualização em XLS',
          'Mostrando' : 'Mostrando',
          'iniciativas' : 'iniciativas',
          'eventos' : 'eventos',
          'Eliminar filtros' : 'Remover filtros',
          //directives/map-filters.html
          'Ciudad' : 'Cidade',
          'Temática' : 'Tema',
          'Espacio' : 'Espaço',
          'Actividad' : 'Atividade',
          'Agente' : 'Agente',
          //directives/search.html
          'Busca por' : 'Pesquisa por',
          'Nombre' : 'Nome',
          'Concepto' : 'Conceito',
          //directives/social-widget.html
          'Perfil de Civics en Facebook' : 'Perfil do Civismo no Facebook',
          'Perfil de Civics en Twitter' : 'Perfil do Civics no Twitter',
          'Repositorio de Civics en Github' : 'Repositório Cívico em Github',
          'Contacta con Civics' : 'Contato Civismo',
          //directives/time-filter.html
          'Todas' : 'Todos',
          'Vigentes' : 'Em vigor',
          'Hoy' : 'Hoje',
          'Mañana' : 'Amanhã',
          'Próximos 7 días' : 'Próximos 7 dias',
          'Próximos 30 días' : 'Próximos 30 dias',
          'Pasadas' : 'Passado',
          'Filtra por fecha' : 'Filtrar por data',
          //services/Categories.js
          'COVID-19' : 'COVID-19',
          'Desarrollo comunitario' : 'Desenvolvimento Comunitário',
          'Arte urbano' : 'Arte urbana',
          'Cultura libre' : 'Cultura livre',
          'Deporte / Salud / Cuidados' : 'Esportes / Saúde / Cuidados',
          'Igualdad / Derechos / Memoria' : 'Igualdade / Direitos / Memória',
          'Medioambiente' : 'Medioambiente',
          'Otras economías' : 'Outras economias',
          'Educación expandida' : 'Educação alternativa',
          'Ciencia / Tecnología' : 'Ciência / Tecnologia',
          'Movilidad sostenible' : 'Mobilidade sustentável',
          'Política y gobernanza' : 'Política e Governança',
          'Urbanismo / Patrimonio' : 'Urbanismo / Patrimônio',
          'Periodismo comunitario' : 'Jornalismo Comunitário',
          'Infancia' : 'Infânzia',
          'Digitalización / Datos Abiertos' : 'Digitalização / Dados Abertos',
          'Feminismos' : 'Feminismos',
          'Centro cultural / comunitario' : 'Centro cultural / comunitário',
          'Efímero e itinerante' : 'Efêmero e itinerante',
          'Intercambio / Trueque' : 'Troca / Trocas',
          'Digital' : 'Digital',
          'Encuentros / Acciones' : 'Reuniões / Ações',
          'Escuelas populares' : 'Escolas populares',
          'Huerto urbano / rural' : 'Pomar urbano / rural',
          'Intervenciones urbanas' : 'Intervenções urbanas',
          'Medios de comunicación comunitaria' : 'Mídia comunitária',
          'Mercado social / Comercios' : 'Mercado Social / Varejo',
          'Solares / Espacios recuperados' : 'Recuperado Solar / Espaços',
          'Labs / Colaborativos / Maker' : 'Labs / Collaborative / Maker',
          'Iniciativas municipales / Gobierno' : 'Iniciativas municipais / Governo',
          'Universidades / ONG / Fundaciones' : 'Universidades / ONGs / Fundações',
          'Organismos internacionales' : 'Organizações internacionais',
          'Empresa social / Startup' : 'Empresa social / Startup',
          'Iniciativa ciudadana' : 'Iniciativa Cidadã',
          'Juntas / Asociaciones de vecinos' : 'Conselhos / Associações',
          'Iniciativas ciudadanas inactivas' : 'Iniciativas cidadanas inativas',
          'Audiovisual' : 'Audiovisual',
          'Curso / Convocatoria' : 'Curso / Chamada',
          'Digital' : 'Digital',
          'Acción' : 'Ação',
          'Evento' : 'Evento',
          'Exposicion' : 'Exposição',
          'Fiesta / Concierto' : 'Festa / Concerto',
          'Publicación' : 'Postagem',
          'Taller' : 'Oficina',
          // help_texts
          'Puedes usar este enlace para compartir la vista actual del mapa' : 'Você pode usar esse link para compartilhar a visualização atual do mapa',
          'Ver contenido en formato lista' : 'Exibir conteúdo no formato de lista',
          'Ver contenido destacado' : 'Exibir conteúdo destacado',
          'Descargar vista actual en formato Excel' : 'Baixar vista atual no formato Excel',
          'Generar un enlace para compartir la vista actual' : 'Gerar um link para compartilhar a visualização atual',
          'Cambiar la capa base del mapa' : 'Alterar mapa base',
          'Volver a la vista inicial de todo el contenido' : 'Voltar para a visão inicial de todo o conteúdo',
          'Localízate en el mapa' : 'Localize-se no mapa',
          'En esta esquina tienes distintas acciones que puedes realizar sobre el contenido mostrado:' : 'Neste canto, você possui diferentes ações que você pode executar no conteúdo mostrado:',
          'Ver contenido en formato mapa' : 'Exibir conteúdo no formato de mapa',
          'Puedes usar este buscador para encontrar iniciativas por nombre (busca coincidencias sólo en los nombres de las iniciativas) o por concepto (busca coincidencias tanto en los nombres como en las descripciones de las iniciativas). Se autocompleta a partir de 3 caracteres insertados' : 'Você pode usar este mecanismo de busca para encontrar iniciativas pelo nome (busca por correspondências apenas nos nomes das iniciativas) ou por conceito (busca por correspondências tanto nos nomes quanto nas descrições das iniciativas). Preenchimento automático a partir de 3 carateres',
          'Usa estos botones para encontrarnos en otras plataformas o contactar con nosotros' : 'Use estes botões para nos encontrar em outras plataformas ou contate-nos',
          'Aquí puedes filtrar los eventos en función de su fecha' : 'Aqui você pode filtrar os eventos de acordo com sua data',
          'Esta es la leyenda del mapa. Puedes pulsar en las ciudades y distintas categorías para filtrar los contenidos visibles según tus intereses' : 'Esta é a lenda do mapa. Você pode clicar nas cidades e categorias diferentes para filtrar os conteúdos visíveis de acordo com seus interesses',
          // Other
          'Promueve' : 'Promove',
          'Saber más sobre' : 'Saiba mais sobre',
          'Iniciativas relacionadas' : 'Iniciativas relacionadas',
          'ODS' : 'ODS',
          'Las iniciativas relacionadas están conectadas por líneas discontinuas con la iniciativa seleccionada' : 'Iniciativas relacionadas são conectadas por linhas tracejadas com a iniciativa selecionada',
          'Objetivos de desarrollo sostenible de la iniciativa' : 'Objetivos de desenvolvimento sustentável da iniciativa',
          'Fin de la pobreza' : 'Erradicaçao da pobreza',
          'Hambre cero' : 'Fome zero',
          'Salud y bienestar' : 'Boa Saúde e bem-estar',
          'Educación de calidad' : 'Educação de qualidade',
          'Igualdad de género' : 'Igualdade de género',
          'Agua limpia y saneamiento' : 'Água limpa e saneamento',
          'Energía asequible y no contaminante' : 'Energía acessível e limpa',
          'Trabajo decente y crecimiento económico' : 'Emprego digno e crescimento económico',
          'Industria, innovación e infraestructura' : 'Industria, inovação e infraestructura',
          'Reducción de las desigualdades' : 'Redução das desigualdades',
          'Ciudades y comunidades sostenibles' : 'Cidades e comunidades sustentáveis',
          'Producción y consumo responsables' : 'Consumo e produção responsáveis',
          'Acción por el clima' : 'Combate ás alterações climáticas',
          'Vida submarina' : 'Vida de baixo d’água',
          'Vida de ecosistemas terrestres' : 'Vida sobre a terra',
          'Paz, justicia e instituciones sólidas' : 'Paz, justiça instituições fortes',
          'Alianzas para lograr los objetivos' : 'Parcerias emproo das metas',
        },
        en: {
            //views/content-list.html
            'Mostrando' : 'Showing',
            'de' : 'of',
            'elementos filtrados' : 'filtered items',
            'Ver página anterior' : 'Go to previous page',
            'Ver página siguiente' : 'Go to next page',
            'Parece que todavía no se han generado contenidos de este tipo' : 'It seems that contents of this type haven\'t been generated yet',
            //views/content-featured.html
            'Volver atrás' : 'Go back',
            'Iniciativas ciudadanas destacadas' : 'Featured civic initiatives',
            'Actividades ciudadanas destacadas' : 'Featured civic activities',
            'Últimas iniciativas ciudadanas incorporadas' : 'Recently published civic initiatives',
            'Próximas actividades ciudadanas' : 'Upcoming civic activities',
            //directives/map-actions.html
            'Usa la leyenda para filtrar los contenidos según tus intereses.' : 'Use the legend to filter content according to your interests.',
            'Ver las iniciativas en formato mapa' : 'See initiatives in map view',
            'Ver las iniciativas en formato lista' : 'See initiatives in list view',
            'Ver las iniciativas destacadas' : 'See featured initiatives',
            'Ver los eventos en formato mapa' : 'See events in map view',
            'Ver los eventos en formato lista' : 'See events in list view',
            'Ver los eventos destacados' : 'See featured events',
            'Descargar la vista en XLS' : 'Download current view in XLS',
            'Mostrando' : 'Showing',
            'iniciativas' : 'initiatives',
            'eventos' : 'events',
            'Eliminar filtros' : 'Remove filters',
            //directives/map-filters.html
            'Ciudad' : 'City',
            'Temática' : 'Topic',
            'Espacio' : 'Space',
            'Actividad' : 'Activity',
            'Agente' : 'Agent',
            //directives/search.html
            'Busca por' : 'Search by',
            'Nombre' : 'Name',
            'Concepto' : 'Concept',
            //directives/social-widget.html
            'Perfil de Civics en Facebook' : 'Civics\' Facebook profile',
            'Perfil de Civics en Twitter' : 'Civics\' Twitter profile',
            'Repositorio de Civics en Github' : 'Repository of civics.cc in Github',
            'Contacta con Civics' : 'Contact Civics team',
            //directives/time-filter.html
            'Todas' : 'All',
            'Vigentes' : 'Current',
            'Hoy' : 'Today',
            'Mañana' : 'Tomorrow',
            'Próximos 7 días' : 'Next 7 days',
            'Próximos 30 días' : 'Next 30 days',
            'Pasadas' : 'Past',
            'Filtra por fecha' : 'Filter by date',
            //services/Categories.js
            'COVID-19' : 'COVID-19',
            'Desarrollo comunitario' : 'Community development',
            'Arte urbano' : 'Urban art',
            'Cultura libre' : 'Free culture',
            'Deporte / Salud / Cuidados' : 'Sport / Health / Personal care',
            'Igualdad / Derechos / Memoria' : 'Equality / Rights / Memory',
            'Medioambiente' : 'Environment',
            'Otras economías' : 'Other economies',
            'Educación expandida' : 'Expanded education',
            'Ciencia / Tecnología' : 'Science / Technology',
            'Movilidad sostenible' : 'Sustainable mobility',
            'Política y gobernanza' : 'Politics and governance',
            'Urbanismo / Patrimonio' : 'Urban planning / Heritage',
            'Periodismo comunitario' : 'Community journalism',
            'Infancia' : 'Childhood',
            'Digitalización / Datos Abiertos' : 'Digitalisation / Open Data',
            'Feminismos' : 'Feminisms',
            'Centro cultural / comunitario' : 'Community / Cultural center',
            'Efímero e itinerante' : 'Ephemeral and itinerant',
            'Intercambio / Trueque' : 'Exchange / Swapping',
            'Digital' : 'Digital',
            'Encuentros / Acciones' : 'Meetings / Actions',
            'Escuelas populares' : 'Community schools',
            'Huerto urbano / rural' : 'Urban / Rural community gardens',
            'Intervenciones urbanas' : 'Urban interventions',
            'Medios de comunicación comunitaria' : 'Community media',
            'Mercado social / Comercios' : 'Social market / Small businesses',
            'Solares / Espacios recuperados' : 'Recovered sites / Spaces',
            'Labs / Colaborativos / Maker' : 'Maker spaces / Collaboratories ',
            'Iniciativas municipales / Gobierno' : 'Municipal initiatives / Government',
            'Universidades / ONG / Fundaciones' : 'Universities / NGO / Foundations',
            'Organismos internacionales' : 'International bodies',
            'Empresa social / Startup' : 'Social company / Startup',
            'Iniciativa ciudadana' : 'Civic initiative',
            'Juntas / Asociaciones de vecinos' : 'Neighbourhood committees / Associations',
            'Iniciativas ciudadanas inactivas' : 'Inactive civic initiatives',
            'Audiovisual' : 'Audiovisual',
            'Curso / Convocatoria' : 'Course / Call',
            'Digital' : 'Digital',
            'Acción' : 'Action',
            'Evento' : 'Event',
            'Exposicion' : 'Exhibition',
            'Fiesta / Concierto' : 'Gig',
            'Publicación' : 'Publication',
            'Taller' : 'Workshop',
            // help_texts
            'Puedes usar este enlace para compartir la vista actual del mapa' : 'You can use this link to share the current map view',
            'Ver contenido en formato lista' : 'See content in list view',
            'Ver contenido destacado' : 'See featured content',
            'Descargar vista actual en formato Excel' : 'Download current view in Excel format',
            'Generar un enlace para compartir la vista actual' : 'Generate a link to share current view',
            'Cambiar la capa base del mapa' : 'Change map base layer',
            'Volver a la vista inicial de todo el contenido' : 'Go back to initial view of content',
            'Localízate en el mapa' : 'Locate yourself in the map',
            'En esta esquina tienes distintas acciones que puedes realizar sobre el contenido mostrado:' : 'Here you have different actions that you can perform on shown content:',
            'Ver contenido en formato mapa' : 'See content in map view',
            'Puedes usar este buscador para encontrar iniciativas por nombre (busca coincidencias sólo en los nombres de las iniciativas) o por concepto (busca coincidencias tanto en los nombres como en las descripciones de las iniciativas). Se autocompleta a partir de 3 caracteres insertados' : 'You can use this widget to find initiatives by name (search for matches only in the names of the initiatives) or by concept (search for matches both in the names and in the descriptions of the initiatives). It autocompletes from 3 inserted characters',
            'Usa estos botones para encontrarnos en otras plataformas o contactar con nosotros' : 'Use these buttons to find us on other platforms or contact us',
            'Aquí puedes filtrar los eventos en función de su fecha' : 'Here you can filter events by date',
            'Esta es la leyenda del mapa. Puedes pulsar en las ciudades y distintas categorías para filtrar los contenidos visibles según tus intereses' : 'This is the legend of the map. You can click on the cities and different categories to filter visible contents according to your interests',
            // Other
            'Promueve' : 'Promoted by',
            'Saber más sobre' : 'Know more about',
            'Iniciativas relacionadas' : 'Related initiatives',
            'ODS' : 'SDG',
            'Las iniciativas relacionadas están conectadas por líneas discontinuas con la iniciativa seleccionada' : 'Related initiatives are connected by dashed lines with the selected initiative',
            'Objetivos de desarrollo sostenible de la iniciativa' : 'Initiative\'s sustainable development goals',
            'Fin de la pobreza' : 'No poverty',
            'Hambre cero' : 'Zero Hunger',
            'Salud y bienestar' : 'Good health and well-being',
            'Educación de calidad' : 'Quality Education',
            'Igualdad de género' : 'Gender Equality',
            'Agua limpia y saneamiento' : 'Clean water and sanitation',
            'Energía asequible y no contaminante' : 'Affordable and clean energy',
            'Trabajo decente y crecimiento económico' : 'Decent work and economic growth',
            'Industria, innovación e infraestructura' : 'Industry, innovation and infrastructure',
            'Reducción de las desigualdades' : 'Reduced Inequalities',
            'Ciudades y comunidades sostenibles' : 'Sustainable cities and communities',
            'Producción y consumo responsables' : 'Responsible consumption and production',
            'Acción por el clima' : 'Climate Action',
            'Vida submarina' : 'Life below water',
            'Vida de ecosistemas terrestres' : 'Life on land',
            'Paz, justicia e instituciones sólidas' : 'Peace, justice and strong institutions',
            'Alianzas para lograr los objetivos' : 'Partnerships for the goals',
          }
    };

    var l = window.location.pathname.split('/')[1];

    return {
        lang : l,

        langs : [
          { k: 'pt', v: 'pt'},
          { k: 'es', v: 'es'},
          { k: 'en', v: 'en'},
        ],

        get: function(text){
            var lang = this.lang;
            return (lang == 'es' || !interfaz[lang] ) ? text : interfaz[lang][text];
        }
    }
});
