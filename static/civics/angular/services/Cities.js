angular.module('civics.cities_service', [])

.factory('Cities', function($http)
{
    return {
        get: function(callback)
        {
            return $http.get('/api/cities').
            then( function(response){
                callback( response );
            }, function(error_response){
                console.log( error_response );
            });
        }
    }
});
