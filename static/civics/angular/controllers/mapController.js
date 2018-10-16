angular.module('civics.map_controller', [])

.controller("MapController", function($scope, Settings, Initiatives, Categories, leafletData, items, meta, DateRanger, XlsDownloader, $route, $location)
{
    /**
     *  Map setup
     */

    // Check url params
    var params = $location.search();

    // Inject resolved data into the map
    var _map = {};
    //  a feature group to hold related initiative connections
    this.relations = new L.FeatureGroup();
    leafletData.getMap("civics-map").then(angular.bind(this, function(map)
    {
        _map = map;
        for(city in items){
            map.addLayer( items[city] );
        }
        this.relations.addTo(map);
    }));

    // Map defaults
    this.defaults = Settings.map_defaults.defaults;
    this.controls = Settings.map_controls;
    this.layers   = Settings.map_layers;
    if(params.center){
        var coords = params.center.split(",");
        this.center = { lat: parseFloat(coords[0]), lng: parseFloat(coords[1]), zoom: parseInt(coords[2]) };
    } else {
        this.center = Settings.map_defaults.center;
    }
    this.highlight_markers = false;

    /**
     *  Section state
     */
    this.count    = meta.count;
    this.section  = meta.showing;
    this.format   = 'map';
    this.show_ods = false;

    // A state to reflect if clusters are fully enabled in current view
    // Map declusters when it reaches the given zoom threshold
    // true : { pruneCluster layer }.Cluster.Size = maximumClusterSize
    // false: { pruneCluster layer }.Cluster.Zoom = minimumClusterSize
    // @see https://github.com/SINTEF-9012/PruneCluster/issues/52#issuecomment-102491577
    var minimumClusterSize = .001;
    var maximumClusterSize = 120;
    var clustersEnabled    = true;
    var zoomThreshold      = 9;

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
    this.ods    = Categories.ods;
    this.spaces = Categories.spaces;
    this.agents = Categories.agents;
    this.activities = Categories.activities;

    // Init filters
    if(this.section == 'initiatives') {
        categories = ['cities', 'topics', 'ods', 'spaces', 'agents' ];
        this.time_scope = 'all';
    } else {
        categories = ['cities', 'topics', 'activities', 'agents' ];
        this.time_scope = 'current';
    }

    // Selected categories
    this.selected_categories = {};
    for(i in categories)
        this.selected_categories[ categories[i] ] = []

    // Selected category tabs
    this.selected_tabs = [];
    for(var i in categories){
        var category = categories[i];
        if(params[category]){
            var subcategories = params[category].split(",");
            if(category=='cities') {
                for(s in subcategories)
                    this.selected_categories['cities'].push( parseInt(subcategories[s]) );
            } else {
                this.selected_categories[ category ] = subcategories;
            }
            for(var j in subcategories){
                if(subcategories[j] !== '') {
                    this.selected_tabs.push({
                        'k' : category,
                        'v' : subcategories[j],
                        'n' : Categories[category][subcategories[j]]
                    });
                }
            }
        }
    }

    // Active elements in legend
    this.active_legend_items = {};

    // Popup states
    this.sharing_url = false;
    this.show_help = false;

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
                    if(this.time_scope != 'all' && !DateRanger.check[this.time_scope](marker.data.date, marker.data.expiration)){
                        marker.filtered = true;
                        c--;
                    }
                }));
            } else {
                markers.forEach( angular.bind(this, function(marker){
                    marker.filtered = false;
                    // Filter by date ranges
                    if(this.time_scope != 'all' &&
                       !DateRanger.check[this.time_scope](marker.data.date, marker.data.expiration)){
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
    this.toggleFilter = function(category, subcategory, city){
        // Disable popups if visible
        this.sharing_url = false;
        this.show_help = false;

        var i = this.selected_categories[category].indexOf(subcategory);

        this.active_legend_items[category][subcategory] = !this.active_legend_items[category][subcategory];
        if(i == -1){
            if(city) {
                this.selected_categories[category].push(parseInt(subcategory));
                this.selected_tabs.push({ 'k' : category, 'v': subcategory, 'n' : city.name });
                _map.setView(city.coords, 10);
            } else {
                this.selected_categories[category].push(subcategory);
                this.selected_tabs.push({ 'k' : category, 'v': subcategory, 'n' : Categories[category][subcategory] });
            }
        } else {
            var i = this.selected_categories[category].indexOf(subcategory);
            this.selected_categories[category].splice(i, 1);
        }
        this.filterMarkers();
        this.show_help = false;
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
        this.sharing_url = false;
        this.show_help = false;
    }

    /**
     *  Remove all filters
     */
    this.removeFilters = function(){
        this.selected_tabs = [];
        this.resetLegend();
        this.filterMarkers();
        this.sharing_url = false;
        this.show_help = false;
    }

    /**
     *   Download XLS with filtered initiatives
     */
    this.download_xls = function(){
        XlsDownloader.get(this.section, this.selected_categories);
        this.sharing_url = false;
        this.show_help = false;
    }


    /**
     *   Reset map view to initial state
     */
    this.expand = function(){
        _map.setView([0, -26], 3);
        this.sharing_url = false;
        this.show_help = false;
    }

    this.shareUrl = function(){
        this.sharing_url = !this.sharing_url;
        this.show_help = false;
        if(this.sharing_url) {
            var base_url = $location.absUrl().split("?")[0];
            this.shared_url = base_url + "?center=" + this.center.lat.toFixed(4) + "," + this.center.lng.toFixed(4) + "," + this.center.zoom;
            for(var category in this.selected_categories){
                var subcategories = this.selected_categories[category];
                if( subcategories.length > 0){
                    this.shared_url += "&" + category + "=";
                    for(var j in subcategories) {
                        this.shared_url += subcategories[j] + ",";
                    }
                }
            }
        }
    }

    $scope.$on('open-marker', angular.bind(this, function(event, args){
        this.sharing_url = false;
        this.show_help = false;
        // Highlight selected initiative and related initiatives
        // Fade all markers
        this.highlight_markers = true;
        // If there's any selected marker unselect it and its related initiatives
        var featured = document.querySelector('.cm.featured');
        if(featured)
          featured.classList.remove('featured');
        var related = document.querySelectorAll('.cm.related');
        if(related) related.forEach( function(initiative){
            initiative.classList.remove('related');
        })
        // Highlight current marker
        var marker   = document.querySelector('.cm--' + args.id);
        marker.classList.add('featured');
        // Highlight related
        for(var i in args.rel){
            var id = args.rel[i].id;
            var m  = document.querySelector('.cm--' + id);
            if(m)
                m.classList.add('related');
        }
        // Draw lines
        leafletData.getMap("civics-map").then(angular.bind(this, function(map)
        {
            this.relations.clearLayers();
            for(var i in args.rel){
                var line =  new L.Polyline([
                    [args.lat, args.lng],
                    [args.rel[i].lat, args.rel[i].lng]
                ], {
                    dashArray : [5, 5],
                    color: '#ed61aa',
                    weight: 2,
                }).addTo(this.relations);
            }

        }));
    }));

    // Unselect markers when closing popup
    $scope.$on('close-marker', angular.bind(this, function(){
          this.highlight_markers = false;
          this.relations.clearLayers();
    }));

    $scope.$on("leafletDirectiveMap.civics-map.moveend", function(event, args) {
        if(args.model.center.zoom >= zoomThreshold && clustersEnabled){
            console.log("Disabling clusters");
            for(var city in items){
               items[city].Cluster.Size   = minimumClusterSize;
               items[city].ProcessView();
            }
            clustersEnabled = false;
        } else if(args.model.center.zoom < zoomThreshold && !clustersEnabled){
            console.log("Disabling clusters");
            for(var city in items){
                items[city].Cluster.Size = maximumClusterSize;
                items[city].ProcessView();
            }
            clustersEnabled = true;
        }
    });
});
