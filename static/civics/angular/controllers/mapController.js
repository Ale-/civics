angular.module('civics.map_controller', [])

.controller("MapController", function(Initiatives, Settings, initiatives, $scope, Categories, leafletData, $location)
{
    this.markers  = initiatives;
    this.defaults = Settings.map_defaults.defaults;
    this.center   = Settings.map_defaults.center;
    this.layers   = Settings.map_layers;
    this.controls = Settings.map_controls;

    this.showing_map = true;

    this.showing_initiative = false;
    this.initiatives_count = this.markers.length;

    this.topics = Categories.topics;
    this.spaces = Categories.spaces;
    this.agents = Categories.agents;

    this.calculating = false;

    /**
     *  Setup visible categories
     */
    this.active = {
      'topics' : {},
      'agents' : {},
      'spaces' : {},
    };

    for(var topic in this.topics)
        this.active['topics'][topic] = true;

    for(var agent in this.agents)
        this.active['agents'][agent] = true;

    for(var space in this.spaces)
        this.active['spaces'][space] = true;

    // for(var i = 0; i < this.initiatives_count; i++){
    //     var marker = this.markers[i];
    //     if(marker.topic != 'otra') this.categories['topics'][marker.topic]['markers'].push(i);
    //     this.categories['agents'][marker['agent']]['markers'].push(i);
    //     if(marker.space != 'x' && marker.space != 'ot') this.categories['spaces'][marker['space']]['markers'].push(i);
    // };


    /**
     *  Add active category to the link in the page header
     */
    var links = document.querySelectorAll(".main-menu__link");
    links[0].setAttribute('class', 'main-menu__link main-menu__link--active-initiatives');
    links[1].setAttribute('class', 'main-menu__link');

    /**
     *  toggle
     *  Implement main functionality in the map filters
     *  Toggles a category showing/hiding markers related to it
     *  TODO: optimize
     */
    this.toggle = function(category, subcategory){
        var count = this.initiatives_count;
        this.active[category][subcategory] = !this.active[category][subcategory];
        this.markers.forEach( angular.bind(this, function(marker){
            if( this.active['topics'][marker.topic] &&
                this.active['agents'][marker.agent] &&
                this.active['spaces'][marker.space]){
                if(marker.layer != marker.original_layer){
                    marker.layer = marker.original_layer;
                    count++;
                }
            } else if(marker.layer != 'hidden'){
                marker.layer = 'hidden';
                count--;
            }
        }));
        this.initiatives_count = count;
    }

    /**
     *   Add click event to map markers to show initiative related information
     */
    var current_marker = {};

    $scope.$on('leafletDirectiveMarker.initiatives-map.click', angular.bind(this, function(event, args){
        this.showing_initiative     = true;
        this.initiative             = args.model;
        this.initiative_topicname   = Categories.topics[args.model.topic];
        this.initiative_agentname   = Categories.agents[args.model.agent];
        this.initiative_spacename   = Categories.spaces[args.model.space];
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

    this.download_xls = function(){
        var base_url = "api/initiatives_xls?topics=";
        for(var topic in this.active.topics)
            if( this.active.topics[topic] == true )
              base_url += topic.toUpperCase() + ",";
        base_url += "&spaces=";
        for(var space in this.active.spaces)
            if( this.active.spaces[space] == true )
              base_url += space.toUpperCase() + ",";
        base_url += "&agents=";
        for(var agent in this.active.agents)
            if( this.active.agents[agent] == true )
              base_url += agent.toUpperCase() + ",";

        window.open(base_url);
    };

});
