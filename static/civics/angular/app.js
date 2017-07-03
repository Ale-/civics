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
    'angular-loading-bar',
    'leaflet-directive',
    'civics.settings',
    'civics.categories_service',
    'civics.initiatives_service',
    'civics.list_service',
    'civics.events_service',
    'civics.map_controller',
    'civics.list_controller',
    'civics.directives',
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
                   return Initiatives.setup()
               }
          }
      })
      .when('/iniciativas-lista', {
          templateUrl : templates_url + 'content-list.html',
          controller  : 'ListController',
          controllerAs: 'content',
          resolve: {
               items: function(Lists) {
                   return Lists.setup('/api/initiatives_list?city=all&topics=all&spaces=all&agents=all', 'initiatives')
               }
          }
      })
      .when('/eventos', {
          templateUrl : templates_url + 'content-map.html',
          controller  : 'MapController',
          controllerAs: 'content',
          resolve: {
              items: function(Events) {
                  var links = document.querySelectorAll('.main-menu__link');
                  links.forEach( function(link){ link.classList.remove('active') })
                  links[2].classList.add('active')
                  return Events.setup();
              }
          }
      })
      .when('/eventos-lista', {
          templateUrl : templates_url + 'content-list.html',
          controller  : 'ListController',
          controllerAs: 'content',
          resolve: {
               items: function(Lists) {
                   var links = document.querySelectorAll('.main-menu__link');
                   links.forEach( function(link){ link.classList.remove('active') })
                   links[2].classList.add('active')
                   return Lists.setup('/api/events_list?city=all&topics=all&categories=all&agents=all', 'events')
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
