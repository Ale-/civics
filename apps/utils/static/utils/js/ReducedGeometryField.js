/**
 *   Custom implementation of Leaflet widget with unnecesary fields
 */

var ReducedGeometryField = L.GeometryField.extend({
    _controlDrawOptions: function () {
        return {
            edit: {
                featureGroup: this.drawnItems
            },
            draw: {
                polyline  : false,
                polygon   : false,
                circle    : false, // Turns off this drawing tool
                rectangle : false,
                marker    : this.options.is_point,
            }
        };
    }
});
