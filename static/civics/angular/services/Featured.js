angular.module('civics.featured_service', [])

.factory('Featured', function($http, meta)
{
    return {
        setup    : function(url, section){
            return $http.get(url).then(angular.bind(this, function(response){
                meta.showing = section;
                return response.data;
            }), function(error_response){
                console.log(error_response);
            });
        }
    }
});
