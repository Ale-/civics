angular.module('civics.initiatives_controller', [])

.controller("InitiativesController", function($scope, Settings, Initiatives, initiatives, Categories, leafletData)
{
    // Map settings
    this.defaults = Settings.map_defaults.defaults;
    this.center   = Settings.map_defaults.center;
    this.controls = Settings.map_controls;
    this.layers   = Settings.map_layers;

    // Section state
    this.showing_map = true;
    this.showing_initiative = false;
    this.initiatives_count = Initiatives.count;

    // Filter categories
    this.cities = Categories.city_initiatives;
    this.topics = Categories.topic;
    this.spaces = Categories.space;
    this.agents = Categories.agent;
    this.active_categories = {
        'city'  : {},
        'topic' : {},
        'space' : {},
        'agent' : {},
    };

    // Active filter tags
    this.active_filters = [];

    //Set active item in menu
    var items = document.querySelectorAll('.main-menu__link');
    items[0].className = 'main-menu__link'
    items[1].className = 'main-menu__link main-menu__link--active'
    items[2].className = 'main-menu__link'

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
        var count = Initiatives.count;
        var filters_length = this.active_filters.length;

        for(city in Initiatives.clusters){
            var markers = Initiatives.clusters[city].Cluster._markers;
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
            Initiatives.clusters[city].ProcessView();
        }
        this.initiatives_count = count;
    };


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

    var _map = {};
    // Add initiative info to map
    leafletData.getMap("initiatives-map").then(angular.bind(this, function(map)
    {
        _map = map;
        for(city in initiatives){
            map.addLayer( initiatives[city] );
        }
    }));

    this.expand = function(){
        _map.setView([0, -26], 3);
    }

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
});
