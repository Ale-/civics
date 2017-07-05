angular.module('civics.list_service', [])

.factory('Lists', function($http, meta, Categories)
{
    return {
        setup    : function(url, section){
            return $http.get(url).then(angular.bind(this, function(response){
                meta.showing = section;
                if('featured' in response.data){
                    meta.count   = response.data.length;
                    var items = response.data;
                } else {
                    var items = [];
                    for(var country in response.data){
                        for(var city in response.data[country]){
                            items.push(...response.data[country][city]);
                            if(section == 'initiatives')
                                Categories.addInitiativeCity(country, city, 0);
                            else
                                Categories.addEventCity(country, city, 0);
                        }
                    }
                    meta.count = items.length;
                }
                return items;
            }), function(error_response){
                console.log(error_response);
            });
        }
    }
});
