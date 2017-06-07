/**
 *  Geocode an address
 */

/**
 *  Builds a GeoJSON string from latitude and longitude coordinates
 */

 function coords_to_geojson(lat, lng){
     return '{"type":"Point", "coordinates":['+ lng + ',' + lat + ']}';
 }

 /**
  *  Make an AJAX GET
  */

 function get(url, callback, error_callback)
 {
     var ajax = new XMLHttpRequest();
     var SUCCESS = 200;

     ajax.onreadystatechange = function() {
         if (ajax.readyState == XMLHttpRequest.DONE) {
             if (ajax.status == SUCCESS) {
                 callback(ajax.response);
             } else if(error_callback){
                 error_callback(ajax.response);
             }
         }
     };
     ajax.open("GET", url, true);
     ajax.send();
 }

 /**
  *  A geocoder object
  */

function Geocoder(map, marker, geometry_field)
 {
     this.google = {
         api : function(params){
             var api_url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + encodeURIComponent(params.address);
             if(params.key)
               api_url += ("&key=" + params.key);
             return api_url;
         },
         callback : function(response){
             var data = JSON.parse(response);
             var lat = data['results'][0]['geometry']['location']['lat'];
             var lng = data['results'][0]['geometry']['location']['lng'];
             if(marker){
                 map.removeLayer(marker);
             }
             marker = L.marker([lat, lng], { 'draggable' : true });
             marker.on('dragend', function(e){
                 var latlng = e.target.getLatLng();
                 geometry_field.value = coords_to_geojson(latlng.lat, latlng.lng);
             });
             map.addLayer(marker).setView([lat, lng], 12);
             geometry_field.value = coords_to_geojson(lat, lng);
         }
     };
     this.nominatim = {
         api      : function(params){
             return  "http://nominatim.openstreetmap.org/search/" + encodeURIComponent(address);
         },
         callback : function(results){
             return;
         }
     };
 }

+(function()
{
    document.querySelectorAll('.geocode-widget').forEach( function(widget)
    {
        var geometry_field  = widget.querySelector('.geocode-widget__geometry');
        if(geometry_field.value){
            var data = JSON.parse(geometry_field.value);
            var map = L.map('geocode-widget__map');
            var marker = L.marker([data.coordinates[1], data.coordinates[0]], { 'draggable' : true });
            marker.on('dragend', function(e){
                var latlng = e.target.getLatLng();
                geometry_field.value = coords_to_geojson(latlng.lat, latlng.lng);
            });
            map.addLayer(marker).setView([data.coordinates[1], data.coordinates[0]], 4);
        } else {
            var map = L.map('geocode-widget__map').setView([-15, -26], 2);
            var marker = {};
        }

        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        var geocoder        = new Geocoder(map, marker, geometry_field);
        var trigger         = widget.querySelector('.geocode-widget__geocode-submit');
        trigger.addEventListener('click', function(e)
        {
            e.stopPropagation();
            var address = '';
            var sources = geometry_field.dataset.sources.split(' ');
            sources.forEach( function(source){
                var el = document.getElementById(source);
                if(el.tagName == 'INPUT')
                    address += el.value;
                else if(el.tagName == 'SELECT')
                    address += el.options[el.selectedIndex].innerHTML;
                address += ", "
            });
            var provider = geometry_field.dataset.provider;
            get(geocoder[provider].api({
                  'address' : address,
                  'key'     : widget.getAttribute('data-key'),
                }), geocoder[provider].callback
            );
        });
    });
})();
