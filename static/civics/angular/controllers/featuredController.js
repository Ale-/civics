angular.module('civics.featured_controller', [])

/**
 *   Controller for list displays
 */
.controller("FeaturedController", function(items, $http, $rootScope, meta, $window)
{
    /**
     *  Section state
     */
    this.featured_items = items.featured;
    this.last_items     = items.last;
    this.section        = meta.showing;
    // Set active links in Django menu
    var links = document.querySelectorAll('.main-menu__link');
    links.forEach( function(link){ link.classList.remove('active') })
    if(this.section == 'initiatives')
        links[1].classList.add('active')
    else
        links[2].classList.add('active')
    // Close responsive menu popup if open
    document.querySelector('.region-toolbar__right').classList.remove('active')

    /**
     *  Breadcrumb
     */
    this.goBack = function(){
        $window.history.back();
    }

    /**
     *  Show popup of selected markers
     */
    this.show = function(marker){
        var url = '/api/initiative?id=';
        if(this.section == 'events')
           url = '/api/event?id=';
        $http.get(url + marker.id, {
            ignoreLoadingBar: true,
        }).then( angular.bind(this, function(response){
            $rootScope.$broadcast('open-marker', response.data);
        }));
    }
});
