angular.module('civics.initiatives_service', [])

.factory('initiatives_data', function($cacheFactory){
    return $cacheFactory('initiatives');
})

.factory('Initiatives', function($http, Settings, Categories, $rootScope, $q, meta, initiatives_data)
{
    var initiatives = {};

    initiatives.createCategories = function(){
        $http.get('/api/cities_with_initiatives', {
            ignoreLoadingBar: true,
        }).then(
            function(response){
                for(var i in response.data){
                  var city = response.data[i];
                  /** Update initiative cities category for the filters */
                  Categories.addInitiativeCity(city.country, city.name, city.id, city.coordinates);
                }
            }
        );
    };

    // Returns a list of events from cached data
    initiatives.createList = function(){
        var items = [];
        var initiatives = initiatives_data.get('initiatives');
        for(var i in initiatives){
            initiative = initiatives[i];
            items.push({
                  name   : initiative.name,
                  pk     : initiative.pk,
                  topics : initiative.topic.toLowerCase(),
                  agents : initiative.agent.toLowerCase(),
                  spaces : initiative.space.toLowerCase(),
                  cities : initiative.city,
                  img    : initiative.image,
            });
        }
        meta.count = items.length;
        return items;
    };

    // Returns a list of clusters from cached data
    initiatives.createClusters = function(){
        PruneCluster.Cluster.ENABLE_MARKERS_LIST = true;
        meta.count = 0;

        var clusters = {};
        var initiatives = initiatives_data.get('initiatives');
        for(var i in initiatives){
            var marker = initiatives[i];
            var city = marker.city;
            if(!(city in clusters)){
                clusters[city] = new PruneClusterForLeaflet();
            }
            var pos = JSON.parse(marker.position);
            var m = new PruneCluster.Marker(pos.coordinates[1], pos.coordinates[0], {
                id     : marker.pk,
                cities : city,
                topics : marker.topic.toLowerCase(),
                spaces : marker.space.toLowerCase(),
                agents : marker.agent.toLowerCase(),
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
                                    "<i class='inner i-sp-" + data.spaces + "'></i>",
                }) );
                leafletMarker.on('click', function(e){
                    $http.get('/api/initiative?id=' + data.id, {
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
    initiatives.setup = function(format){
        meta.showing = 'initiatives';
        this.createCategories();
        if( initiatives_data.get('initiatives') == null ) {
            return $http.get('/api/initiatives', { cache: true }).then( function(response){
                initiatives_data.put('initiatives', JSON.parse(response.data));
                if(format == 'map' ){
                    return initiatives.createClusters();
                } else {
                    return initiatives.createList();
                }
            }, function(error_response){
                console.log(error_response);
            });
        } else {
            return $q( function(resolve, reject){
                if(format == 'map' ){
                    resolve( initiatives.createClusters() );
                } else {
                    resolve( initiatives.createList() );
                }
            }).then( function(clusters) {
                return clusters;
            });
        }
    };

    return initiatives;

});
