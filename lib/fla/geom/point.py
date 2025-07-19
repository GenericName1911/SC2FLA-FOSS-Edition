from lxml.etree import *


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        # attributes
        self.x = x
        self.y = y
    
    def load(self, xml: Element):
        if "x" in xml.attrib:
            self.x = float(xml.attrib["x"])
        
        if "y" in xml.attrib:
            self.y = float(xml.attrib["y"])
    
    def save(self):
        xml = Element("Point")

        if self.x is not None and self.x != 0.0:
            xml.attrib["x"] = str(self.x)
        
        if self.y is not None and self.y != 0.0:
            xml.attrib["y"] = str(self.y)

        return xml
