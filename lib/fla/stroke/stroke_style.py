from lxml.etree import *

from .solid_stroke import SolidStroke

from ..dom import NAMESPACES


class StrokeStyle:
    def __init__(self, index: int = None) -> None:
        self.data: SolidStroke = None
        self.index = index
    
    def load(self, xml: Element):
        if "index" in xml.attrib:
            self.index = int(xml.attrib["index"])
        
        solid_stroke = xml.find("./xfl:SolidStroke", NAMESPACES)
        if solid_stroke is not None:
            self.data = SolidStroke()
            self.data.load(solid_stroke)
    
    def save(self):
        xml = Element("StrokeStyle")

        if self.index is not None:
            xml.attrib["index"] = str(self.index)
        
        if self.data is not None:
            xml.append(self.data.save())

        return xml
