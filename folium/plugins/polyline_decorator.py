# -*- coding: utf-8 -*-

from branca.element import Figure, JavascriptLink

from folium.features import MacroElement
# from folium.utilities import parse_options
from folium.vector_layers import path_options

from jinja2 import Template

_default_js = [
    ('polylinedecorator',
     'https://cdn.jsdelivr.net/npm/leaflet-polylinedecorator@1.6.0/dist/leaflet.polylineDecorator.js')
    ]


class PolyLineDecorator(MacroElement):
    """
    Class for adding decorations to an existing PolyLine.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations:
    **kwargs:
        PolyLineDecorator options.

    See the developer's github repo for more information:
    https://github.com/bbecquet/Leaflet.PolylineDecorator/
    """

    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.polylineDecorator(
              {{ this.locations.get_name() }}, {
              patterns: [
                  {offset: {{ this.offset|tojson }},
                   endOffset: {{ this.end_offset|tojson }},
                   repeat: {{ this.repeat|tojson }},
                   symbol: L.Symbol.arrowHead({
                                        pixelSize: {{  this.pixel_size|tojson }},
                                        polygon: {{ this.polygon|tojson }},
                                        pathOptions: {{ this.options|tojson }}
                           })
                   }
                ]
            }).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)

    def __init__(self, locations, offset=0.0, end_offset=0.0, repeat=0,
                 pixel_size=10, polygon=False,
                 **kwargs):
        super(PolyLineDecorator, self).__init__()
        self._name = 'PolyLineDecorator'
        self.locations = locations
        self.options = path_options(line=True, **kwargs)
        self.offset = offset
        self.end_offset = end_offset
        self.repeat = repeat
        self.pixel_size = pixel_size
        self.polygon = polygon

    def render(self, **kwargs):
        super(PolyLineDecorator, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        # Import Javascripts
        for name, url in _default_js:
            figure.header.add_child(JavascriptLink(url), name=name)
