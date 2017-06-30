angular.module('civics.initiatives_service', [])

.factory('Initiatives', function($http, Settings, Categories, $rootScope, meta)
{
    return {
        clusters : {},

        setup    : function(){
            return $http.get('/api/initiatives?city=all&topics=all&spaces=all&agents=all').then(angular.bind(this, function(response){
                this.clusters = {};
                meta.count = 0;
                meta.showing = 'initiatives';

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
                                'className'   : 'cm',
                                'html'        : "<i class='outer i-to-" + data.topics + " i-ag-" + data.agents + "'></i>" +
                                                "<i class='inner i-sp-" + data.spaces + "'></i>",
                            }));
                            leafletMarker.on('click', function(e){
                                 $rootScope.$broadcast('open-marker', data);
                            });
                        };
                        this.clusters[city].Cluster.Size = 8;

                        /** Setup markers */
                        for(var i = 0, l = response.data[country][city]['items'].length; i < l; i++){
                            var marker = response.data[country][city]['items'][i];
                            // We use three-letter keys to get a lighter data-structure
                            // But we keep full names in categories because they're needed
                            // that way in the controller. @see MapController.js
                            // TODO: get a coherent name logic for controller, categories and markers
                            var m = new PruneCluster.Marker(marker.lat, marker.lng, {
                                id  : marker.id,
                                nam : marker.nam,
                                slu : marker.slu,
                                cou : country,
                                add : marker.add,
                                des : marker.des,
                                //img         : marker.img,
                                web : marker.web,
                                ema : marker.ema,
                                cities : city,
                                topics : marker.top,
                                spaces : marker.spa,
                                agents : marker.age,
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
