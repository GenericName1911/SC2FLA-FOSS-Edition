from lxml.etree import *

from .solid_color import SolidColor
from .linear_gradient import LinearGradient
from .radial_gradient import RadialGradient
from .bitmap_fill import BitmapFill

from ..dom import NAMESPACES


class FillStyle:
    def __init__(self, index: int = None) -> None:
        # attributes
        self.index = index

        # elements
        self.data = None
    
    def load(self, xml: Element):
        if "index" in xml.attrib:
            self.index = int(xml.attrib["index"])
        
        solid_color = xml.find("./xfl:SolidColor", NAMESPACES)
        if solid_color is not None:
            self.data = SolidColor()
            self.data.load(solid_color)
        
        linear_gradient = xml.find("./xfl:LinearGradient", NAMESPACES)
        if linear_gradient is not None:
            self.data = LinearGradient()
            self.data.load(linear_gradient)
        
        radial_gradient = xml.find("./xfl:RadialGradient", NAMESPACES)
        if radial_gradient is not None:
            self.data = RadialGradient()
            self.data.load(radial_gradient)

        bitmap_fill = xml.find("./xfl:BitmapFill", NAMESPACES)
        if bitmap_fill is not None:
            self.data = BitmapFill()
            self.data.load(bitmap_fill)
    
    def save(self):
        xml = Element("FillStyle")

        if self.index is not None:
            xml.attrib["index"] = str(self.index)
        
        if self.data is not None and isinstance(self.data, (SolidColor, LinearGradient, RadialGradient, BitmapFill)):
            xml.append(self.data.save())

        return xml
