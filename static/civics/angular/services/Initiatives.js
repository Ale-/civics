angular.module('civics.initiatives_service', [])

.factory('Initiatives', function($http, Settings)
{
    return {
        markers: [],

        setup: function(){
            // if(this.markers.length > 0)
            //   return this.markers;
            return $http.get('/api/initiatives?city=all&topics=all&spaces=all&agents=all').
            then( angular.bind(this, function(response){
                if(Array.isArray(response.data)){
                    response.data.forEach(function(marker){
                        marker.icon = {
                            'type' : 'div',
                            'iconSize'    : [40, 60],
                            'iconAnchor'  : [20, 60],
                            'popupAnchor' : [0, -30],
                            'message'     : marker.name,
                            'html'        : "<div class='initiative-marker'>" +
                                            "<i class='outer icon-topic-" + marker.topic + " icon-agent-" + marker.agent + "'></i>" +
                                                "<i class='inner icon-space-" + marker.space + "'></i>" +
                                             "</div>",
                        }
                    });
                    this.markers = response.data;
                }
                return this.markers;

            }), function(error_response){
                console.log(error_response);
            });
        },
    }
});
