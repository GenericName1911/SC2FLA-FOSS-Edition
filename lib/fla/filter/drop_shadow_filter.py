from lxml.etree import *


class DrowShadowFilter:
    def __init__(self) -> None:
        # attributes
        self.color: int = 0

        self.strength: float = 0

        self.blur_x: int = None
        self.blur_y: int = None

        self.angle: float = 0.0
        self.distance: int = 0
    
    def load(self, xml: Element):
        if "color" in xml.attrib:
            self.color = int(str(xml.attrib["color"]).replace("#", "0x"), 0)
        
        if "strength" in xml.attrib:
            self.strength = float(xml.attrib["strength"])
        
        if "blurX" in xml.attrib:
            self.blur_x = int(xml.attrib["blurX"])
        
        if "blurY" in xml.attrib:
            self.blur_y = int(xml.attrib["blurY"])
        
        if "angle" in xml.attrib:
            self.angle = float(xml.attrib["angle"])
        
        if "distance" in xml.attrib:
            self.distance = int(xml.attrib["distance"])

    def save(self):
        xml = Element("DrowShadowFilter")

        if self.color is not None:
            xml.attrib["color"] = "#" + str(hex(self.color).lstrip("0x").zfill(6))
        
        if self.strength is not None:
            xml.attrib["strength"] = str(self.strength)
        
        if self.blur_x is not None:
            xml.attrib["blurX"] = str(self.blur_x)
        
        if self.blur_y is not None:
            xml.attrib["blurY"] = str(self.blur_y)
        
        if self.angle is not None:
            xml.attrib["angle"] = str(self.angle)
        
        if self.distance is not None:
            xml.attrib["distance"] = str(self.distance)

        return xml
