angular.module('civics.map_controller', [])

.controller("MapController", function(){

    this.center = {
        lat: 51.505,
        lng: -0.09,
        zoom: 8
    };

});
