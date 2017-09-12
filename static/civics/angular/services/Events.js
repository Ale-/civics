angular.module('civics.events_service', [])

.factory('events_data', function($cacheFactory){
      return $cacheFactory('events');
})

.factory('Events', function($http, Settings, Categories, $rootScope, $q, meta, events_data)
{
    var events = {};

    events.createCategories = function(){
        $http.get('/api/cities_with_events').then(
            function(response){
                for(var i in response.data){
                  var city = response.data[i];
                  /** Update initiative cities category for the filters */
                  Categories.addEventCity(city.country, city.name, city.id, city.coordinates);
                }
            }
        );
    };

    // Returns a list of events from cached data
    events.createList = function(){
        var items = [];
        var events = events_data.get('events');
        for(var i in events){
            items.push( events[i] );
        }
        meta.count = items.length;
        return items;
    };

    // Returns a list of clusters from cached data
    events.createClusters = function(){
        PruneCluster.Cluster.ENABLE_MARKERS_LIST = true;
        meta.count = 0;

        var clusters = {};
        var events = events_data.get('events');
        for(var i in events){
            var marker = events[i];
            var city = marker.fields.city;
            if(!(city in clusters)){
                clusters[city] = new PruneClusterForLeaflet();
            }
            var pos = JSON.parse(marker.fields.position);
            var m = new PruneCluster.Marker(pos.coordinates[1], pos.coordinates[0], {
                id     : marker.pk,
                cities : city,
                topics     : marker.fields.topic.toLowerCase(),
                activities : marker.fields.category.toLowerCase(),
                agents     : marker.fields.agent.toLowerCase(),
            });
            clusters[city].RegisterMarker(m);
            meta.count++;
        }
        for(city in clusters){
            clusters[city].PrepareLeafletMarker = function(leafletMarker, data){
                leafletMarker.setIcon( L.divIcon({
                    'iconSize'    : [40, 60],
                    'iconAnchor'  : [20, 60],
                    'className'   : 'cm',
                    'html'        : "<i class='outer i-to-" + data.topics + " i-ag-" + data.agents + "'></i>" +
                                    "<i class='inner i-ac-" + data.activities + "'></i>",
                }) );
                leafletMarker.on('click', function(e){
                    $http.get('/api/event?id=' + data.id, {
                        ignoreLoadingBar: true,
                    }).then( function(response){
                        $rootScope.$broadcast('open-marker', response.data);
                    });
                });
            };
        }

        return clusters;
    };

    // Fetches data from API and caches it in service data
    // Returns data in the given format
    events.setup = function(format){
        meta.showing = 'events';
        this.createCategories();
        if( !events_data.get('events') ) {
            return $http.get('/api/events', { cache: true }).then( function(response){
                events_data.put('events', JSON.parse(response.data));
                if(format == 'map' ){
                    return events.createClusters();
                } else {
                    return events.createList();
                }
            }, function(error_response){
                console.log(error_response);
            });
        } else {
            return $q( function(resolve, reject){
                if(format == 'map' ){
                    resolve( events.createClusters() );
                } else {
                    resolve( events.createList() );
                }
            }).then( function(clusters) {
                return clusters;
            });
        }
    };

    return events;
});
