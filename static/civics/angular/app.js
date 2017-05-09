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
    'civics.map_controller'
  ])

  .config(['$routeProvider', 'cfpLoadingBarProvider', '$logProvider', '$compileProvider', '$httpProvider', function ($routeProvider, cfpLoadingBarProvider, $logProvider, $compileProvider, $httpProvider) {

    //To avoid excessive amounts of logs coming from the events in leaflet-directive
    $logProvider.debugEnabled(false);

    //To improve performance in production
    $compileProvider.debugInfoEnabled(false);

    //Use applysync to reduce $digest calls using ajax
    $httpProvider.useApplyAsync(true);

    var templates_url = '/static/civics/angular/views/'

    $routeProvider
      .when('/', {
        templateUrl : templates_url + 'map.html',
        controller  : 'MapController',
        controllerAs: 'map',
      })
      .when('/about', {
        templateUrl : templates_url + 'about.html',
        controller  : 'MapController',
        controllerAs: 'map',
      })
      .otherwise({
        redirectTo: '/'
      });
  }]);
