from lxml.etree import *

from ..fill.solid_color import SolidColor

from ..dom import NAMESPACES


class SolidStroke:
    def __init__(self, scale_mode: str = None, weight: float = None) -> None:
        # attributes
        self.scale_mode = scale_mode
        self.weight = weight

        # elements
        self.fill: SolidColor = None
    
    def load(self, xml: Element):
        if "scaleMode" in xml.attrib:
            self.scale_mode = xml.attrib["scaleMode"]
        
        if "weight" in xml.attrib:
            self.weight = float(xml.attrib["weight"])
        
        fill = xml.find("./xfl:fill", NAMESPACES)
        solid_color = fill.find("./xfl:SolidColor", NAMESPACES)

        if solid_color is not None:
            self.fill = SolidColor()
            self.fill.load(solid_color)
    
    def save(self):
        xml = Element("SolidStroke")

        if self.scale_mode is not None:
            xml.attrib["scaleMode"] = str(self.scale_mode)
        
        if self.weight is not None:
            xml.attrib["weight"] = str(self.weight)
        
        if self.fill is not None:
            fill = SubElement(xml, "fill")
            fill.append(self.fill.save())

        return xml
