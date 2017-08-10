angular.module('civics.initiatives_service', [])

.factory('Initiatives', function($http, Settings, Categories, $rootScope, meta)
{
    return {
        clusters : {},

        setup    : function(){
            PruneCluster.Cluster.ENABLE_MARKERS_LIST = true;
            return $http.get('/api/initiatives').then(angular.bind(this, function(response){
                this.clusters = {};
                meta.count = 0;
                meta.showing = 'initiatives';

                for(var country in response.data){
                    for(var city in response.data[country]){
                        /** Update initiative cities category for the filters */
                        Categories.addInitiativeCity(country, city, response.data[country][city]['coordinates']);
                        /** Setup clusters */
                        this.clusters[city] = new PruneClusterForLeaflet();
                        /* Cluster marker icons */
                        this.clusters[city].PrepareLeafletMarker = function(leafletMarker, data){
                            leafletMarker.setIcon( L.divIcon({
                                'iconSize'    : [40, 60],
                                'iconAnchor'  : [20, 60],
                                'className'   : 'cm',
                                'html'        : "<i class='outer i-to-" + data.topics + " i-ag-" + data.agents + "'></i>" +
                                                "<i class='inner i-sp-" + data.spaces + "'></i>",
                            }));
                            leafletMarker.on('click', function(e){
                                $http.get('/api/initiative?id=' + data.id, {
                                    ignoreLoadingBar: true,
                                }).then( angular.bind(this, function(response){
                                    $rootScope.$broadcast('open-marker', response.data);
                                }));
                            });
                        };

                        /* Cluster icons */
                        this.clusters[city].BuildLeafletClusterIcon = function(cluster) {
                            var markers = cluster.GetClusterMarkers();
                            return L.divIcon({
                                'iconSize'    : [40, 40],
                                'iconAnchor'  : [20, 40],
                                'html'        : "<p class='prunecluster'>" + cluster.population + "</p>" +
                                                "<p class='prunecluster__city'>" + markers[0].data.cities + "</p>",
                            });
                        };

                        this.clusters[city].Cluster.Size = 8;

                        /** Setup markers */
                        for(var i = 0, l = response.data[country][city]['items'].length; i < l; i++){
                            var marker = response.data[country][city]['items'][i];
                            var m = new PruneCluster.Marker(marker.lat, marker.lng, {
                                id     : marker.id,
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
