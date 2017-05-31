angular.module('civics.map_controller', [])

.controller("MapController", function(Initiatives, Settings, initiatives, $scope, Categories, leafletData, $location)
{
    // Leaflet map settings
    this.markers  = initiatives;
    this.defaults = Settings.map_defaults.defaults;
    this.center   = Settings.map_defaults.center;
    this.layers   = Settings.map_layers;
    this.controls = Settings.map_controls;

    // Section state
    this.showing_map = true;
    this.showing_initiative = false;
    this.initiatives_count = this.markers.length;

    // Filter categories
    this.cities = Categories.city;
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
        var count = this.markers.length;
        var filters_length = this.active_filters.length;
        if(filters_length > 0){
            this.markers.forEach( angular.bind(this, function(marker)
            {
                let visible = false;
                for(let i = 0; i < filters_length; i++){
                    let filter = this.active_filters[i];
                    if(marker[filter.k] == filter.v){
                        visible = true;
                        break;
                    };
                }
                if(visible){
                    if(marker.layer != marker.city)
                         marker.layer = marker.city;
                } else {
                    marker.layer = 'hidden';
                    count--;
                }
            }));
        } else {
            this.markers.forEach( function(marker){
                if(marker.layer != marker.city)
                     marker.layer = marker.city;
            });
        }
        this.initiatives_count = count;
    };

    /**
     *  Toggle a filter
     */
    this.toggleFilter = function(category, subcategory, city){
        const new_state = !this.active_categories[category][subcategory];
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
     *   Add click event to map markers to show initiative related information
     */
    var current_marker = {};

    $scope.$on('leafletDirectiveMarker.initiatives-map.click', angular.bind(this, function(event, args){
        this.showing_initiative     = true;
        this.initiative             = args.model;
        this.initiative_topicname   = Categories.topic[args.model.topic];
        this.initiative_agentname   = Categories.agent[args.model.agent];
        this.initiative_spacename   = Categories.space[args.model.space];
        if(current_marker)
            current_marker.className = 'leaflet-marker-icon leaflet-div-icon leaflet-zoom-animated leaflet-clickable';
        current_marker              = args.leafletObject._icon;
        current_marker.className    += ' selected';
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
     *   Close initiative information
     */
    this.showInitiativeInfo = function(initiative){
          this.showing_initiative = true
          this.initiative = initiative;
          this.initiative_topicname   = Categories.topics[initiative.topic];
          this.initiative_agentname   = Categories.agents[initiative.agent];
          this.initiative_spacename   = Categories.spaces[initiative.space];
    };

    /**
     *   Download XLS with filtered initiatives
     */
    this.download_xls = function(){
        var base_url = "api/initiatives_xls?topics=";
        for(var topic in this.active_categories.topic)
            if( this.active_categories.topic )
              base_url += topic.toUpperCase() + ",";
        base_url += "&spaces=";
        for(var space in this.active_categories.space)
            if( this.active_categories.space )
              base_url += space.toUpperCase() + ",";
        base_url += "&agents=";
        for(var agent in this.active_categories.agent)
            if( this.active_categories.agent )
              base_url += agent.toUpperCase() + ",";

        window.open(base_url);
    };

});
