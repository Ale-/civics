'use strict';

/**
 * @ngdoc overview
 * @name civics
 * @description
 * Bootstrap Civics angular app
 *
 * Main module of the application.
 */
angular.module('civics', [
    'ngRoute',
    'ngSanitize',
    'angular-loading-bar',
    'leaflet-directive',
    'civics.settings',
    'civics.categories_service',
    'civics.initiatives_service',
    'civics.events_service',
    'civics.featured_service',
    'civics.xls_downloader',
    'civics.map_controller',
    'civics.list_controller',
    'civics.featured_controller',
    'civics.directives',
    'civics.i18n',
  ])

.config(['$routeProvider', 'cfpLoadingBarProvider', '$logProvider', '$compileProvider', '$httpProvider', function ($routeProvider, cfpLoadingBarProvider, $logProvider, $compileProvider, $httpProvider) {

    //To avoid excessive amounts of logs coming from the events in leaflet-directive
    $logProvider.debugEnabled(false);

    //To improve performance in production
    $compileProvider.debugInfoEnabled(false);

    //Use applysync to reduce $digest calls using ajax
    $httpProvider.useApplyAsync(true);

    //Turn off spinner in angular-loading-bar
    cfpLoadingBarProvider.includeSpinner = false;


    var templates_url = '/static/civics/angular/views/'

    $routeProvider
      .when('/iniciativas', {
          templateUrl : templates_url + 'content-map.html',
          controller  : 'MapController',
          controllerAs: 'content',
          resolve: {
               items: function(Initiatives) {
                   return Initiatives.setup('map');
               }
          }
      })
      .when('/iniciativas-lista', {
          templateUrl : templates_url + 'content-list.html',
          controller  : 'ListController',
          controllerAs: 'content',
          resolve: {
               items: function(Initiatives) {
                   return Initiatives.setup('list');
               }
          }
      })
      .when('/iniciativas-destacadas', {
          templateUrl : templates_url + 'content-featured.html',
          controller  : 'FeaturedController',
          controllerAs: 'content',
          resolve: {
               items: function(Featured) {
                   return Featured.setup('/api/initiatives_featured', 'initiatives')
               }
          }
      })
      .when('/eventos', {
          templateUrl : templates_url + 'content-map.html',
          controller  : 'MapController',
          controllerAs: 'content',
          resolve: {
              items: function(Events) {
                  return Events.setup('map');
              }
          }
      })
      .when('/eventos-lista', {
          templateUrl : templates_url + 'content-list.html',
          controller  : 'ListController',
          controllerAs: 'content',
          resolve: {
               items: function(Events) {
                   return Events.setup('list')
               }
          }
      })
      .when('/eventos-destacados', {
          templateUrl : templates_url + 'content-featured.html',
          controller  : 'FeaturedController',
          controllerAs: 'content',
          resolve: {
               items: function(Featured) {
                   return Featured.setup('/api/events_featured', 'events')
               }
          }
      })
      .otherwise({
        redirectTo: '/iniciativas'
      });
}])

.value("meta", {
    'count' : 0,
    'showing' : '',
});
