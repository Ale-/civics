angular.module('civics.events_service', [])

.factory('Events', function($http, Settings){
    return {
        markers: [],

        setup: function(){
            return $http.get('/api/events?city=all&topics=all&categories=all&agents=all').
            then( function(response){
                if(typeof response.data === 'object') {
                    response.data.forEach(function(marker){
                        marker.icon = {
                            'type' : 'div',
                            'iconSize'    : [40, 60],
                            'iconAnchor'  : [20, 60],
                            'popupAnchor' : [0, -30],
                            'message'     : marker.name,
                            'html'        : "<div class='event-marker'>" +
                                            "<i class='outer topic-" + marker.topic + " agent-" + marker.agent + "'></i>" +
                                                "<i class='inner space-" + marker.space + "'></i>" +
                                             "</div>",
                        }
                    });
                    return response.data;
                } else {
                    return [];
                }
            });
        },
    }
});
