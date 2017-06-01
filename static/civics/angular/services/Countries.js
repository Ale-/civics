angular.module('civics.countries_service', [])

.factory('Countries', function($http)
{
    return{
        get: function(callback)
        {
            return $http.get('/api/countries').
            then( function(response){
                callback( response );
            }, function(error_response){
                console.log( error_response );
            });
        }
    }
});
