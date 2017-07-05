angular.module('civics.events_service', [])

.factory('Events', function($http, Settings, Categories, $rootScope, meta)
{
    return {
        clusters : {},

        setup    : function(){
            return $http.get('/api/events').then(angular.bind(this, function(response){
                this.clusters = {};
                meta.count    = 0;
                meta.showing  = 'events';

                for(var country in response.data){
                    for(var city in response.data[country]){
                        /** Update initiative cities category for the filters */
                        Categories.addEventCity(country, city, response.data[country][city]['coordinates']);
                        /** Setup clusters */
                        this.clusters[city] = new PruneClusterForLeaflet();
                        this.clusters[city].PrepareLeafletMarker = function(leafletMarker, data){
                            leafletMarker.setIcon( L.divIcon({
                                'type' : 'div',
                                'iconSize'    : [40, 60],
                                'iconAnchor'  : [20, 60],
                                'popupAnchor' : [0, -30],
                                'className'   : 'cm',  //from civics-marker, cryptic but light (lot of markers)
                                'html'        : "<i class='outer i-to-" + data.topics + " i-ag-" + data.agents + "'></i>" +
                                                "<i class='inner i-ac-" + data.activities + "'></i>",
                            }));
                            leafletMarker.on('click', function(e){
                                $http.get('/api/event?id=' + data.id).then( angular.bind(this, function(response){;
                                    $rootScope.$broadcast('open-marker', response.data);
                                }));
                            });
                        };
                        this.clusters[city].Cluster.Size = 8;

                        /** Setup markers */
                        for(var i = 0, l = response.data[country][city]['items'].length; i < l; i++){
                            var marker = response.data[country][city]['items'][i];
                            var m = new PruneCluster.Marker(marker.lat, marker.lng, {
                                id    : marker.id,
                                cities     : city,
                                topics     : marker.top,
                                agents     : marker.age,
                                activities : marker.act,
                            });
                          this.clusters[city].RegisterMarker(m);
                          meta.count++;
                        }
                    }
                }
                return this.clusters;
            }), function(error_response){
                console.log(error_response);
            });
        }
    }
});
