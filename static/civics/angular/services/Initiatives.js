angular.module('civics.initiatives_service', [])

.factory('Initiatives', function($http, Settings, Categories, $rootScope)
{
    return {
        clusters : {},

        count    : 0,

        setup    : function(){
            return $http.get('/api/initiatives?city=all&topics=all&spaces=all&agents=all').then(angular.bind(this, function(response){
                this.clusters = {};
                this.count    = 0;
                for(var country in response.data){
                    for(var city in response.data[country]){
                        /** Update initiative cities category for the filters */
                        Categories.addInitiativeCity(country, city, response.data[country][city]['coordinates']);
                        /** Setup clusters */
                        this.clusters[city] = new PruneClusterForLeaflet();
                        this.clusters[city].PrepareLeafletMarker = function(leafletMarker, data){
                            leafletMarker.setIcon( L.divIcon({
                                'type' : 'div',
                                'iconSize'    : [40, 60],
                                'iconAnchor'  : [20, 60],
                                'popupAnchor' : [0, -30],
                                'html'        : "<div class='initiative-marker'>" +
                                                "<i class='outer icon-topic-" + data.topic + " icon-agent-" + data.agent + "'></i>" +
                                                    "<i class='inner icon-space-" + data.space + "'></i>" +
                                                 "</div>",
                            }));
                            leafletMarker.on('click', function(e){
                                 $rootScope.$broadcast('open-marker', data);
                            });
                        };
                        this.clusters[city].Cluster.Size = 8;

                        /** Setup markers */
                        for(var i = 0, l = response.data[country][city]['items'].length; i < l; i++){
                            var marker = response.data[country][city]['items'][i];
                            var m = new PruneCluster.Marker(marker.lat, marker.lng, {
                                id          : marker.id,
                                name        : marker.nam,
                                slug        : marker.slu,
                                country     : country,
                                city        : city,
                                address     : marker.add,
                                description : marker.des,
                                //img         : marker.img,
                                website     : marker.web,
                                email       : marker.ema,
                                topic       : marker.top,
                                space       : marker.spa,
                                agent       : marker.age,
                            });
                          this.clusters[city].RegisterMarker(m);
                          this.count++;
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
