from leaflet.forms.widgets import LeafletWidget
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from civics import settings


class ReducedLeafletWidget(LeafletWidget):
    """A custom Leaflet widget, that removes unnecesary feature buttons (polygon, line...)"""

    geometry_field_class = 'ReducedGeometryField'

    class Media:
        """Bind static assets to widget rendering"""
        css = {
            'all': (
                'leaflet/leaflet.css',
                'leaflet/draw/leaflet.draw.css',
            )
        }
        js = (
            'leaflet/leaflet.js',
            'leaflet/leaflet.extras.js',
            'leaflet/draw/leaflet.draw.js',
            'leaflet/leaflet.forms.js',
            'utils/js/ReducedGeometryField.js',
        )


class GeocodedLeafletWidget(forms.widgets.Textarea):
    """A custom leaflet widget, that geocodes its geolocation from other fields"""

    def __init__(self, attrs=None, submit_text='Localiza los datos introducidos', provider='google', sources=None, key=None):
        self.submit_text = submit_text
        self.provider    = provider
        self.sources     = sources
        self.key         = key
        super(GeocodedLeafletWidget, self).__init__(attrs)

    class Media:
        """Bind static assets to widget rendering"""
        css = {
            'all': (
                'leaflet/leaflet.css',
            )
        }
        js = ( 'leaflet/leaflet.js', 'utils/js/geocode.js')

    def render(self, name, value, attrs=None):
        """Render widget"""
        attrs['class'] = 'geocode-widget__geometry'
        attrs['data-provider'] = self.provider
        attrs['data-sources']  = self.sources
        attrs['data-key']      = self.key
        parent_widget = super(GeocodedLeafletWidget, self).render(name, value, attrs )
        geocode = render_to_string("geocoded-leaflet-widget.html", {
            'parent_widget' : parent_widget,
            'submit_text'   : self.submit_text,
        })
        return geocode

class LimitedTextareaWidget(forms.widgets.Textarea):
    """A custom widget, to preview video iframes from an external service as vimeo or youtube"""

    def __init__(self, attrs=None, limit=500):
        self.limit = limit
        super(LimitedTextareaWidget, self).__init__(attrs)

    class Media:
        """Bind static assets to widget rendering"""
        js = ('utils/js/limitedTextarea.js',)

    def render(self, name, value, attrs=None):
        """Render widget"""
        attrs['maxlength'] = self.limit
        parent_widget = super(LimitedTextareaWidget, self).render(name, value, attrs)
        limited_textarea_widget = render_to_string("limited-textarea-widget.html", {
            'parent_widget': parent_widget,
            'limit' : self.limit,
        })
        return limited_textarea_widget


class VideoWidget(forms.widgets.TextInput):
    """A custom widget, to preview video iframes from an external service as vimeo or youtube"""

    def __init__(self, attrs=None, width=640, height=480):
        self.width  = width
        self.height = height
        super(VideoWidget, self).__init__(attrs)

    class Media:
        """Bind static assets to widget rendering"""
        js = ('utils/js/createIframe.js', 'utils/js/videoLoader.js')

    def render(self, name, value, attrs=None):
        """Render widget"""

        parent_widget = super(VideoWidget, self).render(name, value, attrs)
        video_widget = render_to_string("video-widget.html", {
            'parent_widget' : parent_widget,
            'width'         : self.width,
            'height'        : self.height,
        })
        return video_widget


class PictureWithPreviewWidget(forms.widgets.ClearableFileInput):
    """A custom widget, to preview video iframes from an external service as vimeo or youtube"""

    class Media:
         """Bind static assets to widget rendering"""
         js = ('utils/js/picturePreview.js',)

    def render(self, name, value, attrs=None):
        """Render widget"""

        parent_widget = super(PictureWithPreviewWidget, self).render(name, value, attrs )
        picture_preview = render_to_string("picture-preview-widget.html", {
            'id'            : attrs['id'],
            'parent_widget' : parent_widget,
            'value'         : value
        })
        return picture_preview


class SelectOrAddWidget(forms.Select):
    """A widget that extends regular select with an icon to launch a popup to add new options."""

    def __init__(self, attrs=None, view_name=None, link_text="+"):
        self.view_name = view_name
        self.link_text = link_text
        super(SelectOrAddWidget, self).__init__(attrs)

    class Media:
        """Bind static assets to widget rendering"""
        js = ('https://code.jquery.com/jquery-3.2.1.slim.min.js', 'utils/js/RelatedObjectLookups.js' )

    def render(self, name, *args, **kwargs):
        parent_widget = super(SelectOrAddWidget, self).render(name, *args, **kwargs)
        select_or_add_widget = render_to_string("select-or-add-widget.html", {
            'field'         : name,
            'view_name'     : self.view_name,
            'link_text'     : self.link_text,
            'parent_widget' : parent_widget
        })
        return select_or_add_widget

class SelectOrAddMultipleWidget(forms.SelectMultiple):
    """A widget that extends regular select multiple with an icon to launch a popup to add new options."""

    def __init__(self, attrs=None, view_name=None):
        self.view_name = view_name
        super(SelectOrAddMultipleWidget, self).__init__(attrs)

    class Media:
        """Bind static assets to widget rendering"""
        js = ('https://code.jquery.com/jquery-3.2.1.slim.min.js', 'utils/js/RelatedObjectLookups.js' )

    def render(self, name, *args, **kwargs):
        parent_widget = super(SelectOrAddMultipleWidget, self).render(name, *args, **kwargs)
        select_or_add_multiple_widget = render_to_string("select-or-add-widget.html", {
            'field'         : name,
            'view_name'     : self.view_name,
            'link_text'     : self.link_text,
            'parent_widget' : parent_widget
        })
        return select_or_add_multiple_widget
