angular.module('civics.settings', [])

.service('Settings', function($http){

      this.map_defaults = {
          center: {
              lat  : 0,
              lng  : -26,
              zoom : 3,
          },
          defaults: {
              markerZoomAnimation : true,
              zoomAnimation       : true,
              scrollWheelZoom     : true,
              minZoom             : 2,
              maxZoom             : 18,
              controls            : {
                  scale  : { position: 'topright' },
              }
          }
      };

      cities = ["buenos-aires", "rosario", "rio-de-janeiro", "santos", "sao-paulo", "bogota", "cartagena-de-indias", "medellin", "quibdo", "san-jose", "quito", "san-salvador", "madrid", "zaragoza", "santa-fe", "ciudad-de-guatemala", "tegucigalpa", "managua", "montevideo"];

      var overlays = {};



      this.map_layers = {
          baselayers: {
              civics: {
                   name: 'civics',
                   url: 'https://api.mapbox.com/styles/v1/civics/cir1q2kud001icmm9tmh4s9lt/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2l2aWNzIiwiYSI6ImNpcXpmZ2toZTAwNmFpOG1nc2swdG5kZ28ifQ.P6-IjrcLcdnPqQvkn0GWKQ',
                   type: 'xyz',
              },
              toner : {
                  name         : 'Toner',
                  url          : 'https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
                  layerOptions : {
                       attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, \
                                    under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. \
                                    Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, \
                                    under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'
                  },
                  type: 'xyz',
              },
              mapnik : {
                  name         : 'Open Street Map',
                  url          : 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
                  layerOptions : {
                       attribution : '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                  },
                  type : 'xyz',
              },
          },
          overlays: {
              hidden: {
                  name    : 'Hidden markers',
                  visible : false,
                  type    : 'group',
              }
          }
      };

      this.map_controls = {
          custom: [
              L.control.locate({ follow: true })
          ]
      };

      this.setCities = function(cities)
      {
          cities.forEach( angular.bind(this, function(city){
              this.map_layers.overlays[city.name] = {
                  name                    : city.name,
                  visible                 : true,
                  type                    : "markercluster",
                  layerOptions            : {
                      disableClusteringAtZoom : 10,
                      iconCreateFunction: function(cluster) {
                           return L.divIcon({
                              iconSize   : [28, 40],
                              iconAnchor : [14, 40],
                              className  : 'city',
                              html: '<div class="initiative-cluster"> \
                                          <div class="inner"></div> \
                                          <p class="initiative-cluster__name">' +
                                              city.name +
                                          '</p>\
                                          <p class="initiative-cluster__count">' +
                                              cluster.getChildCount() + ' iniciativas\
                                          </p>\
                                     </div>'
                           });
                      },
                      showCoverageOnHover : false,
                  },
              }
          }));
      };

      return this;

});
