angular.module('civics.map_controller', [])

.controller("MapController", function($scope, Settings, Initiatives, Categories, leafletData, items, meta)
{
    /**
     *  Map setup
     */
    // Inject resolved data into the map
    var _map = {};
    leafletData.getMap("civics-map").then(angular.bind(this, function(map)
    {
        _map = map;
        for(city in items){
            map.addLayer( items[city] );
        }
    }));
    // Map defaults
    this.defaults = Settings.map_defaults.defaults;
    this.center   = Settings.map_defaults.center;
    this.controls = Settings.map_controls;
    this.layers   = Settings.map_layers;

    /**
     *  Section state
     */
    this.count = meta.count;
    this.section = meta.showing;
    this.format  = 'map';
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
     *  Setup categories and filter settings
     */
    if(this.section == 'initiatives')
        this.cities = Categories.city_initiatives;
    else
        this.cities = Categories.city_events;
    this.topics = Categories.topics;
    this.spaces = Categories.spaces;
    this.agents = Categories.agents;
    this.activities = Categories.activities;

    if(this.section == 'initiatives')
      categories = ['topics', 'spaces', 'agents' ]
    else
      categories = ['topics', 'activities', 'agents' ]

    this.active_categories = { 'cities' : {} }
    for(i in categories)
        this.active_categories[ categories[i] ] = {}

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
        var filters_length = this.active_filters.length;

        for(city in items){
            var markers = items[city].Cluster._markers;
            if(filters_length > 0){
                markers.forEach( angular.bind(this, function(marker){
                    marker.filtered = false;
                    for(var i = 0; i < filters_length; i++){
                        var filter = this.active_filters[i];
                        if(marker.data[filter.k] != filter.v){
                            marker.filtered = true
                            this.count--;
                            break;
                        }
                    }
                }));
            } else {
                markers.forEach( angular.bind(this, function(marker){
                    marker.filtered = false;
                }));
            }
            items[city].ProcessView();
        }
    };

    /**
     *  Toggle a filter
     */
    this.toggleFilter = function(category, subcategory, city, coordinates){
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
        if(coordinates){
            _map.setView(coordinates, 10);
        }
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

    /**
     *   Reset map view to initial state
     */
    this.expand = function(){
        _map.setView([0, -26], 3);
    }
});
