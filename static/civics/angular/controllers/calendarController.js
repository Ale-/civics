angular.module('civics.calendar_controller', [])

.controller("CalendarController", function($scope, Settings, Events, events, Categories, leafletData)
{

    this.defaults = Settings.map_defaults.defaults;
    this.center   = Settings.map_defaults.center;
    this.controls = Settings.map_controls;
    this.layers   = Settings.map_layers;

    // Section state
    this.showing_map = true;
    this.showing_initiative = false;
    this.events_count = Events.count;

    // Filter categories
    this.cities     = Categories.city_events;
    this.topics     = Categories.topic;
    this.agents     = Categories.agent;
    this.activities = Categories.activity;
    this.active_categories = {
      'city'     : {},
      'topic'    : {},
      'agent'    : {},
      'activity' : {},
    };

    // Active filter tags
    this.active_filters = [];

    //Set active item in menu
    var items = document.querySelectorAll('.main-menu__link');
    items[0].className = 'main-menu__link'
    items[1].className = 'main-menu__link'
    items[2].className = 'main-menu__link main-menu__link--active'

    /**
     *  Reset categories to default inactive state
     */
    this.resetCategories = function(){
        for(var country in this.cities){
            for(var i in this.cities[country]){
                this.active_categories['city'][ this.cities[country][i] ] = false;
            }
        }
        for(var topic in this.topics){
          this.active_categories['topic'][topic] = false;
        }
        for(var space in this.spaces){
          this.active_categories['space'][space] = false;
        }
        for(var agent in this.agents){
          this.active_categories['agent'][agent] = false;
        }
    }
    // Apply default state
    this.resetCategories();

    /**
     *  Filter markers by active categories
     */
    this.filterMarkers = function()
    {
        var count = Events.count;
        var filters_length = this.active_filters.length;

        for(city in Events.clusters){
            var markers = Events.clusters[city].Cluster._markers;
            if(filters_length > 0){
                markers.forEach( angular.bind(this, function(marker){
                    marker.filtered = false;
                    for(var i = 0; i < filters_length; i++){
                        var filter = this.active_filters[i];
                        if(marker.data[filter.k] != filter.v){
                            marker.filtered = true
                            count--;
                            break;
                        }
                    }
                }));
            } else {
                markers.forEach( angular.bind(this, function(marker){
                    marker.filtered = false;
                }));
            }
            Events.clusters[city].ProcessView();
        }
        this.events_count = count;
    };

    /**
     *  Toggle a filter
     */
    this.toggleFilter = function(category, subcategory, city){
        var new_state = !this.active_categories[category][subcategory];
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
     *   Show initiative information
     */
     $scope.$on('open-marker', angular.bind(this, function(event, args){
          this.showing_initiative = true;
          this.initiative = args;
          this.initiative_topicname   = Categories.topics[ this.initiative.topic ];
          this.initiative_agentname   = Categories.agents[ this.initiative.agent ];
          this.initiative_spacename   = Categories.spaces[ this.initiative.space ];
     }));

    /**
     *   Close initiative information
     */
    this.closeInitiativeInfo = function(){
        this.showing_initiative = false;
        current_marker.className = 'leaflet-marker-icon leaflet-div-icon leaflet-zoom-animated leaflet-clickable';
        leafletData.getMap().then(function(map) {
            map.closePopup();
        });
    };

    /**
     *   Download XLS with filtered initiatives
     */
    this.download_xls = function(){
        var base_url = "api/events_xls?topics=";
        for(var topic in this.active_categories.topic)
            if( this.active_categories.topic[topic] )
              base_url += topic.toUpperCase() + ",";
        base_url += "&activities=";
        for(var activity in this.active_categories.activity)
            if( this.active_categories.activity[activity] )
              base_url += activity.toUpperCase() + ",";
        base_url += "&agents=";
        for(var agent in this.active_categories.agent)
            if( this.active_categories.agent[agent] )
              base_url += agent.toUpperCase() + ",";
        window.open(base_url);
    };

    // Add event info to map
    leafletData.getMap("events-map").then(function(map)
    {
        for(city in events){
            map.addLayer( events[city] );
        }
    });

});
