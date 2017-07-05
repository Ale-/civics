angular.module('civics.list_controller', [])

/**
 *   Controller for list displays
 */
.controller("ListController", function(items, Categories, meta, $scope, $rootScope, $http, DateRanger)
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

    if(this.section == 'initiatives'){
        this.cities = Categories.city_initiatives;
    } else {
        this.cities = Categories.city_events;
    }
    this.topics     = Categories.topics;
    this.spaces     = Categories.spaces;
    this.agents     = Categories.agents;
    this.activities = Categories.activities;


    if(this.section == 'initiatives')
      categories = ['cities', 'topics', 'spaces', 'agents' ]
    else
      categories = ['cities', 'topics', 'activities', 'agents' ]

    // Selected categories
    this.selected_categories = {};
    for(i in categories)
        this.selected_categories[ categories[i] ] = []

    // Selected category tabs
    this.selected_tabs = [];

    // Active elements in legend
    this.active_legend_items = {};

    // Needed to filter events by date ranges
    this.time_scope = 'all';

    /**
     *  Reset categories to default inactive state
     */
    this.resetLegend = function(){
        for(var i in categories){
            this.active_legend_items[categories[i]] = {};
            for(var s in this[categories[i]]){
                this.active_legend_items[categories[i]][s] = false;
            }
        }
    }

    // Apply default state
    this.resetLegend();

    this.filterMarkers = function()
    {
        var c = meta.count;
        var filters_length = this.selected_tabs.length;
        var today = new Date();

        if(filters_length > 0){
            items.forEach( angular.bind(this, function(marker){
                // Filter by category
                for(var cat in this.selected_categories){
                    // Every marker is visible by default in each category
                    marker.filtered = false;
                    // If marker category is not in active list filter it
                    if(this.selected_categories[cat].length > 0 &&
                       this.selected_categories[cat].indexOf(marker[cat]) == -1){
                        marker.filtered = true;
                        c--;
                        break;
                    }
                }
                // Filter by date ranges
                if(this.time_scope != 'all' && !DateRanger.check[this.time_scope](today, new Date(marker.dat))){
                    marker.filtered = true;
                    c--;
                }
            }));
        } else {
            items.forEach( angular.bind(this, function(marker){
                marker.filtered = false;
                if(this.time_scope != 'all' && !DateRanger.check[this.time_scope](today, new Date(marker.dat))){
                    marker.filtered = true;
                    c--;
                }
            }));
            for(var cat in this.selected_categories){
                this.selected_categories[cat] = [];
            }
        }
        this.count = c;
    };

    /**
     *   Time filters
     */
    $scope.$on('filter_by_date', angular.bind(this, function(event, args){
        this.time_scope = args.query;
        this.filterMarkers();
    }));

    /**
     *  Toggle a filter
     */
    this.toggleFilter = function(category, subcategory, city, coordinates){
        var i = this.selected_categories[category].indexOf(subcategory);

        this.active_legend_items[category][subcategory] = !this.active_legend_items[category][subcategory];
        if(i == -1){
            this.selected_categories[category].push(subcategory);
            this.selected_tabs.push({ 'k' : category, 'v': subcategory, 'n' : city ? subcategory : Categories[category][subcategory] });
        } else {
            var i = this.selected_categories[category].indexOf(subcategory);
            this.selected_categories[category].splice(i, 1);
        }
        this.filterMarkers();
    }

    /**
     *  Remove a filter
     */
    this.removeFilter = function(index){
        var f = this.selected_tabs.splice(index, 1);
        var i = this.selected_categories[f[0].k].indexOf(f[0].v);
        this.selected_categories[f[0].k].splice(i, 1);
        this.filterMarkers();
    }

    /**
     *  Remove all filters
     */
    this.removeFilters = function(){
        this.selected_tabs = [];
        this.resetLegend();
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
        for(var topic in this.selected_categories.topics)
            if( this.selected_categories.topics[topic] )
              base_url += topic.toUpperCase() + ",";
        if(this.section == 'initiatives'){
            base_url += "&spaces=";
            for(var space in this.selected_categories.spaces)
                if( this.selected_categories.spaces[space] )
                  base_url += space.toUpperCase() + ",";
        } else {
          base_url += "&activities=";
          for(var activity in this.selected_categories.activities)
              if( this.selected_categories.activities[activity] )
                base_url += activity.toUpperCase() + ",";
        }
        base_url += "&agents=";
        for(var agent in this.selected_categories.agent)
            if( this.selected_categories.agent[agent] )
              base_url += agent.toUpperCase() + ",";

        // Get items in new window
        window.open(base_url);
    };

});
