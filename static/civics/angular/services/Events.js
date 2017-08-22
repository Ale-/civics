angular.module('civics.events_service', [])

.factory('Events', function($http, Settings, Categories, $rootScope, $q, meta)
{
    return {
        // Cached data of events
        data : {},

        // Sets up event categories from cached data
        createCategories : function(){
            for(var country in this.data){
                for(var city in this.data[country]){
                    /** Update initiative cities category for the filters */
                    Categories.addEventCity(country, city, this.data[country][city]['coordinates']);
                }
            }
        },

        // Returns a list of events from cached data
        createList : function(){
            var items = [];
            for(var country in this.data){
                for(var city in this.data[country]){
                    items.push(...this.data[country][city]['items']);
                }
            }
            meta.count = items.length;
            return items;
        },

        // Returns a list of clusters from cached data
        createClusters : function(){
            var clusters = {};
            meta.count    = 0;

            for(var country in this.data){
                for(var city in this.data[country]){
                    /** Setup clusters */
                    clusters[city] = new PruneClusterForLeaflet();
                    clusters[city].PrepareLeafletMarker = function(leafletMarker, data){
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
                            $http.get('/api/event?id=' + data.id, {
                                ignoreLoadingBar: true,
                            }).then( angular.bind(this, function(response){;
                                $rootScope.$broadcast('open-marker', response.data);
                            }));
                        });
                    };
                    clusters[city].Cluster.Size = 8;

                    /** Setup markers */
                    for(var i = 0, l = this.data[country][city]['items'].length; i < l; i++){
                        var marker = this.data[country][city]['items'][i];
                        var m = new PruneCluster.Marker(marker.lat, marker.lng, {
                            id    : marker.id,
                            cities     : city,
                            topics     : marker.top,
                            agents     : marker.age,
                            activities : marker.act,
                        });
                      clusters[city].RegisterMarker(m);
                      meta.count++;
                    }
                }
            }
            return clusters;
        },

        // Fetches data from API and caches it in service data
        // Returns data in the given format
        setup : function(format){
            meta.showing = 'events';
            if(Object.keys(this.data).length === 0) {
                return $http.get('/api/events').then( angular.bind(this, function(response){
                    this.data = response.data;
                    this.createCategories();
                    if(format == 'map' ){
                        return this.createClusters();
                    } else {
                        return this.createList();
                    }
                }), function(error_response){
                    console.log(error_response);
                });
            } else {
                return $q( angular.bind(this, function(resolve, reject){
                    if(format == 'map') {
                        resolve( this.createClusters() );
                    } else {
                        resolve( this.createList() );
                    }
                })).then( function(clusters) {
                    return clusters;
                });
            }
        }

    }
});
