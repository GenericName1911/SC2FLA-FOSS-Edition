from lxml.etree import *


class SolidColor:
    def __init__(self, color: int = None, alpha: float = None) -> None:
        # attributes
        self.color = color
        self.alpha = alpha
    
    def load(self, xml: Element):
        if "color" in xml.attrib:
            self.color = int(xml.attrib["color"].replace("#", "0x"), 0)
        
        if "alpha" in xml.attrib:
            self.alpha = float(xml.attrib["alpha"])
    
    def save(self):
        xml = Element("SolidColor")

        if self.color is not None:
            xml.attrib["color"] = "#" + str(hex(self.color).lstrip("0x").zfill(6))
        
        if self.alpha is not None:
            xml.attrib["alpha"] = str(self.alpha)

        return xml
