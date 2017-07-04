// Load the Facebook Graph SDK asynchronously
(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

/**
 *  This is called with the results from from FB.getLoginStatus()
 *  @see dashboard.html
 */
function statusChangeCallback(response, id) {
  if (response.status === 'connected'){
    fetchEvents(id);
  } else {
    $('.facebook-events__help').show() ;
  }
}

// Login to Facebook
function fb_login(){
    FB.login( function(reponse){
        fetchEvents();
    }, { scope: 'user_events' });
}

//Get the Django CSRF token
function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
              var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
           }
        }
    }
    return cookieValue;
}

//New Facebook events
var fb_events = [];

/**
 *  Invoked to add a Facebook event to Django database
 *   @see apps/api/views
 */
function add_to_events(index){
    data = fb_events[index];
    // We have to pass django's CSRF token to receive 200 response
    data['csrfmiddlewaretoken'] = getCookie('csrftoken');
    // Get event activity
    data['category'] = $('#e-act-' + index).val();
    console.log(data['activity']);
    $.post('/api/event_create', data, function(response){
        var object_id = parseInt(response);
        window.location = '/edita/evento/' + object_id;
    });
}

//Util function to format dates properly
function pad(n) {return n<10 ? '0' + n : n}

/**
 *  Fetch events from FB.
 *  Format and store them in an array to be imported to Django
 */
function fetchEvents(id) {
    FB.api('/me/events', function(response){
        events = response.data;
        $('.facebook-events__help').hide();
        // Check if event ID is already in Django database
        // to show only new events
        $.get('/api/events_fb_id', {}, function(response){
            for(i in events){
                var e = events[i];
                if(response.indexOf(e.id) > -1 || response.length == 0){
                    var date = new Date(e.start_time)
                    var event = {
                        name           : e.name,
                        description    : e.description,
                        formatted_date : date.getFullYear()  + "-" + pad(date.getMonth()+1) + "-" + pad(date.getDate()),
                        time           : date.toLocaleTimeString(),
                        lat            : e.place.location.latitude,
                        lon            : e.place.location.longitude,
                        city           : e.place.location.city,
                        address        : e.place.name,
                        facebook_id    : e.id,
                        initiative_id  : id,
                    };
                    fb_events.push(event);
                    console.log(fb_events);
                    var element = '<li class="facebook-events__item">' +
                      "<p class='facebook-events__item-name'>" + event.name + "</p>" +
                      "<p class='facebook-events__item-date'>Fecha: " + event.formatted_date +
                      " a las " + event.time + "</p>" +
                      "<div class='facebook-events__select'>\
                      Elige el tipo de actividad:\
                      <select id='e-act-" + i + "'><option value='AU'>Audiovisual</option>\
                      <option value='CU'>Curso/convocatoria</option>\
                      <option value='DI'>Digital</option>\
                      <option value='EN'>Encuentro</option>\
                      <option value='EV'>Evento</option>\
                      <option value='EX'>Exposición</option>\
                      <option value='FI'>Fiesta / Concierto</option>\
                      <option value='PU'>Publicación</option>\
                      <option value='TA'>Taller</option>\
                      </select></div>\
                      <span onclick='add_to_events(i)'>Importa este evento</span>\
                      </li>";
                    $('.facebook-events__list').append(element);
                }
            }
            if(fb_events.length == 0){
                  $('.facebook-events__empty').show();
            }
        });
    });
}
