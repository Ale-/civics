angular.module('civics.events_service', [])

.factory('Events', function($http, Settings){
    return {
        markers: [],

        setup: function(){
            return $http.get('/api/events?city=all&topics=all&categories=all&agents=all').
            then( angular.bind(this, function(response){
                if(Array.isArray(response.data)){
                    response.data.forEach(function(marker){
                        marker.icon = {
                            'type' : 'div',
                            'iconSize'    : [40, 60],
                            'iconAnchor'  : [20, 60],
                            'popupAnchor' : [0, -30],
                            'message'     : marker.title,
                            'html'        : "<div class='initiative-marker'>" +
                                            "<i class='outer icon-topic-" + marker.topic + " icon-agent-" + marker.agent + "'></i>" +
                                                "<i class='inner icon-category-" + marker.category + "'></i>" +
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
