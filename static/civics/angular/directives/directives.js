/**
 *  Get this script path to use relative paths for templates and avoid breaking
 *  the site because of the changes i18n introduces in paths (language prefixes)
 *  @see https://stackoverflow.com/questions/21103724/angular-directive-templateurl-relative-to-js-file
 */
var scripts = document.getElementsByTagName("script")
var path    = scripts[scripts.length-1].src;  //last script is the one being evaluated

angular.module('civics.directives', [])

/**
 *  Social widget block
 */
.directive('social', function(){
    return {
      restrict: 'A',
      templateUrl: path.replace('directives.js', 'social_widget.html')
      //templateUrl: 'static/civics/angular/directives/social_widget.html'
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
        templateUrl: path.replace('directives.js', 'marker-info.html'),
        //templateUrl: 'static/civics/angular/directives/marker-info.html',
        replace: true
    }
})

.controller('MarkerinfoController', function(Categories, $scope, meta, $sce){
     /** Video */
     /** Root scope event fired from the services that create the markers **/
     $scope.$on('open-marker', angular.bind(this, function(event, args){
          this.expanded = true;
          this.marker = args;
          this.media_src = $sce.trustAsResourceUrl(this.marker.vid);
          this.marker.topicname = Categories.topics[ this.marker.topics ];
          this.marker.agentname = Categories.agents[ this.marker.agents ];
          if(this.marker.spaces)
              this.marker.spacename = Categories.spaces[ this.marker.spaces ];
          if(this.marker.activities)
              this.marker.activitiesname = Categories.activities[ this.marker.activities ];
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
        templateUrl: path.replace('directives.js', 'map-actions.html'),
        //templateUrl: 'static/civics/angular/directives/map-actions.html'
    }
})

/**
 *  Marker information in the maps
 */
.directive('leafletExpand', function(){
    return {
        restrict: 'A',
        replace: true,
        template: '<div class="leaflet-expand" ng-click="content.expand()"><span class="icon-expand"></span></div>',
    }
})

/**
 *  Marker information in the maps
 */
.directive('mapFilters', function(){
    return {
        restrict: 'A',
        replace: true,
        templateUrl: path.replace('directives.js', 'map-filters.html'),
        //templateUrl: 'static/civics/angular/directives/map-filters.html'
    }
})

/**
 *  Marker information in the maps
 */
.directive('search', function(){
    return {
        restrict: 'A',
        replace: true,
        controller: 'SearchController',
        controllerAs: 'search',
        templateUrl: path.replace('directives.js', 'search.html'),
        //templateUrl: 'static/civics/angular/directives/search.html'
    }
})

.controller('SearchController', function($scope, $http, $rootScope, leafletData){
     this.results = [];

     this.query = function(){
        if(this.name.length > 2){
            $http.get('/api/autocomplete?n=' + this.name, {
                ignoreLoadingBar: true,
            }).then( angular.bind(this, function(response){
                if(response.data.length > 0)
                    this.results = response.data;
            }));
        } else {
            this.results = [];
        }
     };

     this.set = function(id){
        $http.get('/api/initiative?id=' + id).then( angular.bind(this, function(response){;
            $rootScope.$broadcast('open-marker', response.data);
            leafletData.getMap('civics-map').then(function(map){
                map.setView([response.data.lat, response.data.lng], 18)
            });
            this.results = [];
            this.name    = '';
        }));
     };
})

/**
 *  Marker information in the maps
 */
.directive('timeFilter', function(){
    return {
        restrict: 'A',
        replace: true,
        controller: 'TimefilterController',
        controllerAs: 'timefilter',
        templateUrl: path.replace('directives.js', 'time-filter.html'),
        //templateUrl: 'static/civics/angular/directives/time-filter.html'
    }
})

.controller('TimefilterController', function($rootScope){
    this.results = [];
    this.query = 'current';
    this.filter = function(){
        $rootScope.$broadcast('filter_by_date', { query : this.query });
    }
})

.service('DateRanger', function(){
    var day = 24 * 60 * 60 * 1000;
    var today = new Date().getTime();
    this.check = {
        'current' : function(date, expiration){
            if(!expiration)
                return date >= today;
            return date >= today || expiration > today;
        },
        'today' : function(date, expiration){
            if(!expiration)
                return date == today;
            return today > date  && today < expiration;
        },
        'tomorrow' : function(date, expiration){
            var tomorrow   = today + day;
            if(!expiration)
                return date == tomorrow;
            return tomorrow > date && tomorrow < expiration;
        },
        'next_week' : function(date, expiration){
            var week_end   = today + 7 * day;
            if(!expiration)
                return date > today && date < week_end;
            return (expiration > today && expiration < week_end ) ||
                   (date > today && date < week_end ) ||
                   (date < today && expiration > week_end );
        },
        'next_month' : function(date, expiration){
            var month_end   = today + 30 * day;
            if(!expiration)
                return date > today && date < month_end;
            return (date > today && expiration < month_end ) ||
                   (date > today && date < month_end ) ||
                   (date < today && expiration > month_end );
        },
        'past' : function(date, expiration){
            if(!expiration)
                return date < today;
            return date < today && expiration < today;
        }
    }

    return this;
})

/**
 *  Dates overlay in event grid views
 */
.directive('dates', function(){
    return {
        restrict    : 'A',
        replace     : true,
        templateUrl : path.replace('directives.js', 'dates.html'),
        scope       : {
            date       : "@",
            expiration : "@",
        },
    }
})
