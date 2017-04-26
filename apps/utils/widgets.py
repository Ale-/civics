from leaflet.forms.widgets import LeafletWidget

class ReducedLeafletWidget(LeafletWidget):
    """A custom Leaflet widget, that removes unnecesary feature buttons (polygon, line...)"""

    geometry_field_class = 'ReducedGeometryField'
