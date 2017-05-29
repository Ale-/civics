angular.module('civics.calendar_controller', [])

.controller("CalendarController", function(Events, Settings, events, $scope, Categories)
{
    this.markers  = [];
    this.defaults = Settings.map_defaults.defaults;
    this.center   = Settings.map_defaults.center;
    this.layers   = Settings.map_layers;
    this.controls = Settings.map_controls;

    this.showing_event = false;
    this.events_count = this.markers.length;

    this.topics     = Categories.topics;
    this.activities = Categories.activities;
    this.agents     = Categories.agents;

    this.active = {
      'topics'     : {},
      'agents'     : {},
      'activities' : {},
    };

    for(var topic in this.topics){
      this.active['topics'][topic] = true;
    }
    for(var agent in this.agents){
      this.active['agents'][agent] = true;
    }
    for(var activity in this.activities){
      this.active['activities'][activity] = true;
    }

    var links = document.querySelectorAll(".main-menu__link");
    links[1].setAttribute('class', 'main-menu__link main-menu__link--active-calendar');
    links[0].setAttribute('class', 'main-menu__link');

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
                this.active['activities'][marker.activity] &&
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
     *   Add mouseout event to map markers to hide the popup
     */
    $scope.$on('leafletDirectiveMarker.initiatives-map.click', angular.bind(this, function(event, args){
        this.showing_event = true;
    }));
});
