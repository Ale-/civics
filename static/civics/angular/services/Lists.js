angular.module('civics.list_service', [])

.factory('Lists', function($http, meta)
{
    return {
        setup    : function(url, section){
            return $http.get(url).then(angular.bind(this, function(response){
                meta.showing = section;
                meta.count   = response.data.length;
                return response.data;
            }), function(error_response){
                console.log(error_response);
            });
        }
    }
});
