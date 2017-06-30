angular.module('civics.map_controller', [])

.controller("MapController", function($scope, Settings, Initiatives, Categories, leafletData, items, meta)
{

    // Inject resolved data into the map
    var _map = {};
    leafletData.getMap("civics-map").then(angular.bind(this, function(map)
    {
        _map = map;
        for(city in items){
            map.addLayer( items[city] );
        }
    }));

    // Map settings
    this.defaults = Settings.map_defaults.defaults;
    this.center   = Settings.map_defaults.center;
    this.controls = Settings.map_controls;
    this.layers   = Settings.map_layers;

    // Section state
    this.showing_map = true;
    this.initiatives_count = meta.count;
    this.section = meta.showing;

    // Filter categories
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
        this.initiatives_count = meta.count;
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
                            this.initiatives_count--;
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
    this.download_xls = function(){
        var base_url = "api/initiatives_xls?topics=";
        for(var topic in this.active_categories.topic)
            if( this.active_categories.topic[topic] )
              base_url += topic.toUpperCase() + ",";
        base_url += "&spaces=";
        for(var space in this.active_categories.space)
            if( this.active_categories.space[space] )
              base_url += space.toUpperCase() + ",";
        base_url += "&agents=";
        for(var agent in this.active_categories.agent)
            if( this.active_categories.agent[agent] )
              base_url += agent.toUpperCase() + ",";
        window.open(base_url);
    };

    // /**
    //  *   Download XLS with filtered events
    //  */
    // this.download_xls = function(){
    //     var base_url = "api/events_xls?topics=";
    //     for(var topic in this.active_categories.topic)
    //         if( this.active_categories.topic[topic] )
    //           base_url += topic.toUpperCase() + ",";
    //     base_url += "&activities=";
    //     for(var activity in this.active_categories.activity)
    //         if( this.active_categories.activity[activity] )
    //           base_url += activity.toUpperCase() + ",";
    //     base_url += "&agents=";
    //     for(var agent in this.active_categories.agent)
    //         if( this.active_categories.agent[agent] )
    //           base_url += agent.toUpperCase() + ",";
    //     window.open(base_url);
    // };

    this.expand = function(){
        _map.setView([0, -26], 3);
    }

    //Set active item in menu
    // var items = document.querySelectorAll('.main-menu__link');
    // items[0].className = 'main-menu__link'
    // items[1].className = 'main-menu__link main-menu__link--active'
    // items[2].className = 'main-menu__link'
});
