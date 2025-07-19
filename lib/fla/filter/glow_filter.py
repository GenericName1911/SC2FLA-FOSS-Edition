from lxml.etree import *


class GlowFilter:
    def __init__(self) -> None:
        # attributes
        self.color: int = 0

        self.strength: int = 0

        self.blur_x: int = None
        self.blur_y: int = None
    
    def load(self, xml: Element):
        if "color" in xml.attrib:
            self.color = int(str(xml.attrib["color"]).replace("#", "0x"), 0)
        
        if "strength" in xml.attrib:
            self.strength = int(xml.attrib["strength"])
        
        if "blurX" in xml.attrib:
            self.blur_x = int(xml.attrib["blurX"])
        
        if "blurY" in xml.attrib:
            self.blur_y = int(xml.attrib["blurY"])

    def save(self):
        xml = Element("GlowFilter")

        if self.color is not None:
            xml.attrib["color"] = "#" + str(hex(self.color).lstrip("0x").zfill(6))
        
        if self.strength is not None:
            xml.attrib["strength"] = str(self.strength)
        
        if self.blur_x is not None:
            xml.attrib["blurX"] = str(self.blur_x)
        
        if self.blur_y is not None:
            xml.attrib["blurY"] = str(self.blur_y)

        return xml
