from lxml.etree import *


class GradientEntry:
    def __init__(self, color: int = None, ratio: float = None) -> None:
        # attributes
        self.color = color
        self.ratio = ratio
    
    def load(self, xml: Element):
        if "color" in xml.attrib:
            self.color = int(xml.attrib["color"].replace("#", "0x"), 0)
        
        if "ratio" in xml.attrib:
            self.ratio = float(xml.attrib["ratio"])
    
    def save(self):
        xml = Element("GradientEntry")

        if self.color is not None:
            xml.attrib["color"] = "#" + str(hex(self.color).lstrip("0x").zfill(6))
        
        if self.ratio is not None:
            xml.attrib["ratio"] = str(self.ratio)

        return xml
