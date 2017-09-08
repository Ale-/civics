angular.module('civics.initiatives_service', [])

.factory('initiatives_data', function($cacheFactory){
      return $cacheFactory('items');
})

.factory('Initiatives', function($http, Settings, Categories, $rootScope, $q, meta, initiatives_data)
{

    var initiatives = {};
    // Returns a list of events from cached data

    initiatives.createList = function(){
        var items = [];
        var initiatives = initiatives_data.get('items');
        for(var i in initiatives){
            items.push( initiatives[i] );
        }
        meta.count = items.length;
        return items;
    };

    // Returns a list of clusters from cached data
    initiatives.createClusters = function(){
        PruneCluster.Cluster.ENABLE_MARKERS_LIST = true;
        meta.count = 0;

        var clusters = {};
        var initiatives = initiatives_data.get('items');
        for(var i in initiatives){
            var marker = initiatives[i];
            var city = marker.fields.city;
            if(!(city in clusters)){
                clusters[city] = new PruneClusterForLeaflet();
            }
            clusters[city].PrepareLeafletMarker = function(leafletMarker, data){
                leafletMarker.setIcon( L.divIcon({
                    'iconSize'    : [40, 60],
                    'iconAnchor'  : [20, 60],
                    'className'   : 'cm',
                    'html'        : "<i class='outer i-to-" + data.topics + " i-ag-" + data.agents + "'></i>" +
                                    "<i class='inner i-sp-" + data.spaces + "'></i>",
                }) );
                leafletMarker.on('click', function(e){
                    $http.get('/api/initiative?id=' + marker.pk, {
                        ignoreLoadingBar: true,
                    }).then( function(response){
                        $rootScope.$broadcast('open-marker', response.data);
                    });
                });
            };
            var pos = JSON.parse(marker.fields.position);
            var m = new PruneCluster.Marker(pos.coordinates[1], pos.coordinates[0], {
                id     : marker.pk,
                cities : city,
                topics : marker.fields.topic.toLowerCase(),
                spaces : marker.fields.space.toLowerCase(),
                agents : marker.fields.agent.toLowerCase(),
            });
            clusters[city].RegisterMarker(m);
            meta.count++;
        }
        return clusters;
    };

    // Fetches data from API and caches it in service data
    // Returns data in the given format
    initiatives.setup = function(format){
        meta.showing = 'initiatives';
        console.log( initiatives_data.get('items') );
        if( !initiatives_data.get('items') ) {
            return $http.get('/api/initiatives', { cache: true }).then( function(response){
                initiatives_data.put('items', JSON.parse(response.data));
                //this.createCategories();
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
