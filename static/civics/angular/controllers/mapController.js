angular.module('civics.map_controller', [])

.controller("MapController", function($scope, Settings, Initiatives, Categories, leafletData, items, meta, DateRanger, XlsDownloader, $route)
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
    for(var i=0; i < links.length; ++i){
        links[i].classList.remove('active');
    }

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

    /**
     *  Filter markers by active categories
     */
    this.filterMarkers = function()
    {
        var c = meta.count;
        var filters_length = this.selected_tabs.length;
        var today = new Date();

        for(city in items){
            var markers = items[city].Cluster._markers;
            if(filters_length > 0){
                markers.forEach( angular.bind(this, function(marker){
                    for(var cat in this.selected_categories){
                        // Every marker is visible by default in each category
                        marker.filtered = false;
                        // If marker category is not in active list filter it
                        if(this.selected_categories[cat].length > 0 &&
                           this.selected_categories[cat].indexOf(marker.data[cat]) == -1){
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
                markers.forEach( angular.bind(this, function(marker){
                    marker.filtered = false;
                    // Filter by date ranges
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
            items[city].ProcessView();
        }
    };

    this.filterMarkers();

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
        if(coordinates){
            _map.setView(coordinates, 10);
        }
    }

    /**
     *  Remove a filter
     */
    this.removeFilter = function(index){
        var f = this.selected_tabs.splice(index, 1);
        var i = this.selected_categories[f[0].k].indexOf(f[0].v);
        this.selected_categories[f[0].k].splice(i, 1);
        this.active_legend_items[f[0].k][f[0].v] = false;
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
     *   Download XLS with filtered initiatives
     */
    this.download_xls = function(){
        XlsDownloader.get(this.section, this.selected_categories);
    }


    /**
     *   Reset map view to initial state
     */
    this.expand = function(){
        _map.setView([0, -26], 3);
    }
});
