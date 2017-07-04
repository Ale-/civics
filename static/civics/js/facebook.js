function fb_login(){
    FB.login( function(reponse){
        fetchEvents();
    }, { scope: 'user_events' });
}

// This is called with the results from from FB.getLoginStatus().
  function statusChangeCallback(response, id) {
      if (response.status === 'connected'){
          fetchEvents(id);
      } else {
          $('.facebook-events__help').show() ;
      }
  }

  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
  // code below.
  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }

  // Load the SDK asynchronously
  (function(d, s, id) {
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return;
      js = d.createElement(s); js.id = id;
      js.src = "//connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  //Get the CSRF token
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
  var fb_events = [];

  function add_to_events(index){
      data = fb_events[index];
      data['csrfmiddlewaretoken'] = getCookie('csrftoken');
      $.post('/api/event_create', data, function(response){
          var object_id = parseInt(response);
          window.location = '/edita/evento/' + object_id;
      });
  }

  function pad(n) {return n<10 ? '0' + n : n}

  // Here we run a very simple test of the Graph API after login is
  // successful.  See statusChangeCallback() for when this call is made.
  function fetchEvents(id) {
      FB.api('/me/events', function(response){
          events = response.data;
          $('.facebook-events__help').hide();
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
                      var element = '<li class="facebook-events__item" onclick="add_to_events(i)">' +
                        "<p class='facebook-events__item-name'>" + event.name + "</p>" +
                        "<p class='facebook-events__item-date'>Fecha: " + event.formatted_date +
                        " a las " + event.time + "</p>" +
                        "<p class='facebook-events__item-add'></li>";
                      $('.facebook-events__list').append(element);
                  }
              }
              if(fb_events.length == 0){
                    $('.facebook-events__empty').show();
              }
          });
      });
  }
