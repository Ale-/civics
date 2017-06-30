angular.module('civics.directives', [])

/**
 *  Social widget block
 */
.directive('social', function(){
    return {
      restrict: 'A',
      templateUrl: 'static/civics/angular/views/social_widget.html'
    }
})

/**
 *  Marker information in the maps
 */
.directive('markerInfo', function(){
    return {
        restrict: 'A',
        controller: 'MarkerinfoController',
        controllerAs: 'info',
        templateUrl: 'static/civics/angular/views/marker-info.html',
        replace: true
    }
})

.controller('MarkerinfoController', function(Categories, $scope, meta){
     /** Root scope event fired from the services that create the markers **/
     $scope.$on('open-marker', angular.bind(this, function(event, args){
          this.expanded = true;
          this.marker = args;
          this.marker.topicname = Categories.topic[ this.marker.topic ];
          this.marker.agentname = Categories.agent[ this.marker.agent ];
          this.marker.spacename = Categories.space[ this.marker.space ];
          this.showing = meta.showing;
     }));
})

/**
 *  Marker information in the maps
 */
.directive('mapActions', function(){
    return {
        restrict: 'A',
        replace: true,
        templateUrl: 'static/civics/angular/views/map-actions.html'
    }
})

/**
 *  Marker information in the maps
 */
.directive('leafletExpand', function(){
    return {
        restrict: 'A',
        replace: true,
        template: '<div class="leaflet-expand" ng-click="map.expand()"><span class="icon-expand"></span></div>',
    }
})

/**
 *  Marker information in the maps
 */
.directive('mapFilters', function(){
    return {
        restrict: 'A',
        replace: true,
        templateUrl: 'static/civics/angular/views/map-filters.html'
    }
});
