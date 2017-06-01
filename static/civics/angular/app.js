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
    'civics.initiatives_service',
    'civics.categories_service',
    'civics.events_service',
    'civics.cities_service',
    'civics.countries_service',
    'civics.map_controller',
    'civics.calendar_controller',
  ])

  .run( function(Cities, Countries, Categories, Settings){
      Cities.get( function(cities_response){;
          Categories.setCities( cities_response.data );
          Settings.setCities( cities_response.data );
      });
      Countries.get( function(countries_response){;
          Settings.setCountries( countries_response.data );
      });
  })

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
          templateUrl : templates_url + 'initiatives.html',
          controller  : 'MapController',
          controllerAs: 'map',
          resolve: {
              initiatives: function(Initiatives) {
                  return Initiatives.setup();
              }
          }
      })
      .when('/eventos', {
          templateUrl : templates_url + 'calendar.html',
          controller  : 'CalendarController',
          controllerAs: 'calendar',
          resolve: {
              events: function(Events) {
                  return Events.setup();
              }
          }
      })
      .when('/about', {
        templateUrl : templates_url + 'about.html',
        controller  : 'MapController',
        controllerAs: 'map',
      })
      .otherwise({
        redirectTo: '/iniciativas'
      });
  }]);
