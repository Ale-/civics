angular.module('civics.list_controller', [])

/**
 *   Controller for list displays
 */
.controller("ListController", function(items, Categories, meta, $rootScope, $http)
{
    /**
     *  Content setup
     */
    this.markers = items;
    for(i in this.markers)
      this.markers[i].filtered = false;  // Show markers by default

    /**
     *  Section state
     */
    this.showing_map = true;
    this.count = this.markers.length;
    this.section = meta.showing;
    this.format  = 'list';
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
     *  Pager setup and methods
     */
    this.starting_index = 0;
    this.items_per_page = 50;
    this.starting_index = 0;
    this.ending_index   = this.items_per_page;
    this.current_items  = 0;

    // Get previous results
    this.previousPage = function(){
        var next_index = this.starting_index - this.items_per_page;
        this.starting_index = next_index < 0 ? 0 : next_index;
        this.set_current_items();
    }
    // Get next results
    this.nextPage = function(){
        var next_index = this.starting_index + this.items_per_page;
        this.starting_index = next_index > this.count ? this.starting_index : next_index;
        this.set_current_items();
    }
    // Get number of current displayed elements
    this.set_current_items = function(){
        var factor = parseFloat(this.count - this.starting_index)/parseFloat(this.items_per_page);
        this.current_items = factor > 1 ? this.items_per_page : this.count - this.starting_index;
    }
    this.set_current_items();

    /**
     *  Setup categories and filter settings
     */
    if(this.section == 'initiatives')
        this.cities = Categories.city_initiatives;
    else
        this.cities = Categories.city_events;
    this.topics     = Categories.topics;
    this.spaces     = Categories.spaces;
    this.agents     = Categories.agents;
    this.activities = Categories.activities;

    if(this.section == 'initiatives')
      categories = ['topics', 'spaces', 'agents' ]
    else
      categories = ['topics', 'activities', 'agents' ]

    this.active_categories = { 'cities' : {} }
    for(i in categories)
        this.active_categories[ categories[i] ] = {}

    // Active filter tags
    this.active_filters = [];

    /**
     *  Reset categories to default inactive state
     */
    this.resetCategories = function(){
        for(var country in this.cities){
            for(var i in this.cities[country]){
                this.active_categories['cities'][ this.cities[country][i] ] = false;
            }
        }
        for(var cat in categories){
            for(var val in this[cat])
                this.active_categories[cat][val] = false;
        }
    }

    // Apply default state
    this.resetCategories();

    /**
     *  Filter markers by active categories
     */
    this.filterMarkers = function()
    {
        this.count = meta.count;
        this.starting_index = 0;
        console.log(this.active_filters);
        var filters_length = this.active_filters.length;
        if(filters_length > 0){
            this.markers.forEach( angular.bind(this, function(marker){
                marker.filtered = false;
                for(var i = 0; i < filters_length; i++){
                    var filter = this.active_filters[i];
                    if(marker[filter.k] != filter.v){
                        marker.filtered = true
                        this.count--;
                        break;
                    }
                }
            }));
        } else {
            this.markers.forEach( angular.bind(this, function(marker){
                marker.filtered = false;
            }));
        }
        this.set_current_items();
    };

    /**
     *  Toggle a filter
     */
    this.toggleFilter = function(category, subcategory, city){
        var new_state = !this.active_categories[category][subcategory];
        for(var s in this.active_categories[category]){
            if(this.active_categories[category][s]){
               this.active_categories[category][s] = false;
               for(var i = 0; i < this.active_filters.length; i++ )
                  if(this.active_filters[i].k == category && this.active_filters[i].v == s){
                      this.active_filters.splice(i,1);
                      break;
                  }
               break;
             }
        }
        this.active_categories[category][subcategory] = new_state;
        if(new_state)
            this.active_filters.push({ 'k' : category, 'v': subcategory, 'n' : city ? subcategory : Categories[category][subcategory] });
        else {
            var index = this.active_filters.findIndex(function(filter){
                return filter.v == subcategory;
            });
            this.active_filters.splice(index, 1);
        }
        this.filterMarkers();
    }

    /**
     *  Remove a filter
     */
    this.removeFilter = function(index){
        this.active_filters.splice(index, 1);
        this.filterMarkers();
    }

    /**
     *  Remove all filters
     */
    this.removeFilters = function(){
        this.active_filters = [];
        this.resetCategories();
        this.filterMarkers();
    }

    /**
     *  Show popup of selected markers
     */
    this.show = function(marker){
         var url = '/api/initiative?id=';
         if(this.section == 'events')
            url = '/api/event?id=';
         $http.get(url + marker.id).then( angular.bind(this, function(response){
             $rootScope.$broadcast('open-marker', response.data);
         }));
    }

    /**
     *   Download XLS with filtered initiatives
     */
    this.download_xls = function()
    {
        // Check section and build base URL for the query
        var base_url = "api/initiatives_xls?topics=";
        if(this.section == 'events')
            base_url = "api/events_xls?topics=";

        // Build url
        for(var topic in this.active_categories.topics)
            if( this.active_categories.topics[topic] )
              base_url += topic.toUpperCase() + ",";
        if(this.section == 'initiatives'){
            base_url += "&spaces=";
            for(var space in this.active_categories.spaces)
                if( this.active_categories.spaces[space] )
                  base_url += space.toUpperCase() + ",";
        } else {
          base_url += "&activities=";
          for(var activity in this.active_categories.activities)
              if( this.active_categories.activities[activity] )
                base_url += activity.toUpperCase() + ",";
        }
        base_url += "&agents=";
        for(var agent in this.active_categories.agent)
            if( this.active_categories.agent[agent] )
              base_url += agent.toUpperCase() + ",";

        // Get items in new window
        window.open(base_url);
    };

});
