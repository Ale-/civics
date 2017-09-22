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
          'Busca por nombre' : 'Pesquisar por nome',
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
          'Desarrollo comunitario' : 'Desenvolvimento Comunitário',
          'Arte urbano' : 'Arte urbana',
          'Cultura libre' : 'Cultura livre',
          'Deporte / Salud / Cuidados' : 'Esportes / Saúde / Cuidados',
          'Igualdad / Derechos / Memoria' : 'Igualdade / Direitos / Memória',
          'Ecología / Consumo' : 'Ecologia / Consumo',
          'Otras economías' : 'Outras economias',
          'Educación expandida' : 'Educação alternativa',
          'Ciencia / Tecnología' : 'Ciência / Tecnologia',
          'Movilidad sostenible' : 'Mobilidade sustentável',
          'Política y gobernanza' : 'Política e Governança',
          'Urbanismo / Patrimonio' : 'Urbanismo / Patrimônio',
          'Periodismo comunitario' : 'Jornalismo Comunitário',
          'Centro cultural / comunitario' : 'Centro cultural / comunitário',
          'Efímero e itinerante' : 'Ephemeral e itinerante',
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
          'Conquistas ciudadanas del pasado' : 'Realizações do passado',
          'Audiovisual' : 'Audiovisual',
          'Curso / Convocatoria' : 'Curso / Chamada',
          'Digital' : 'Digital',
          'Encuentro' : 'Encontro',
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
          'Puedes usar este buscador para encontrar iniciativas por su nombre. Se autocompleta a partir de 3 caracteres insertados' : 'Você pode usar este mecanismo de busca para encontrar iniciativas pelo nome. Autocompletar de 3 caracteres inseridos',
          'Usa estos botones para encontrarnos en otras plataformas o contactar con nosotros' : 'Use estes botões para nos encontrar em outras plataformas ou contate-nos',
          'Aquí puedes filtrar los eventos en función de su fecha' : 'Aqui você pode filtrar os eventos de acordo com sua data',
          'Esta es la leyenda del mapa. Puedes pulsar en las ciudades y distintas categorías para filtrar los contenidos visibles según tus intereses' : 'Esta é a lenda do mapa. Você pode clicar nas cidades e categorias diferentes para filtrar os conteúdos visíveis de acordo com seus interesses',
        }
    };

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
