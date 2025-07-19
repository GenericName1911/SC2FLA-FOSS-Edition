from lxml.etree import *

from .color_transform import ColorTransform


class Color(ColorTransform):
    def __init__(self) -> None:
        super().__init__()
    
    def load(self, xml: Element):
        if "redMultiplier" in xml.attrib:
            self.red_multiplier = float(xml.attrib["redMultiplier"])
        
        if "redOffset" in xml.attrib:
            self.red_offset = int(xml.attrib["redOffset"])
        
        if "greenMultiplier" in xml.attrib:
            self.green_multiplier = float(xml.attrib["greenMultiplier"])
        
        if "greenOffset" in xml.attrib:
            self.green_offset = int(xml.attrib["greenOffset"])
        
        if "blueMultiplier" in xml.attrib:
            self.blue_multiplier = float(xml.attrib["blueMultiplier"])
        
        if "blueOffset" in xml.attrib:
            self.blue_offset = int(xml.attrib["blueOffset"])
        
        if "alphaMultiplier" in xml.attrib:
            self.alpha_multiplier = float(xml.attrib["alphaMultiplier"])
        
        if "alphaOffset" in xml.attrib:
            self.alpha_offset = int(xml.attrib["alphaOffset"])
        
        if "tintColor" in xml.attrib:
            self.red_multiplier = 0
            self.green_multiplier = 0
            self.blue_multiplier = 0

            color = int(xml.attrib["tintColor"].replace("#", "0x"), 0)

            self.red_offset = (color & 0xFF0000) >> 16
            self.green_offset = (color & 0x00FF00) >> 8
            self.blue_offset = (color & 0x0000FF) >> 0
        
        if "tintMultiplier" in xml.attrib:
            multiplier = 1 - float(xml.attrib["tintMultiplier"])

            self.red_multiplier = multiplier
            self.green_multiplier = multiplier
            self.blue_multiplier = multiplier
    
    def save(self):
        xml = Element("Color")

        if self.red_multiplier is not None:
            xml.attrib["redMultiplier"] = str(self.red_multiplier)
        
        if self.red_offset is not None:
            xml.attrib["redOffset"] = str(self.red_offset)
        
        if self.green_multiplier is not None:
            xml.attrib["greenMultiplier"] = str(self.green_multiplier)
        
        if self.green_offset is not None:
            xml.attrib["greenOffset"] = str(self.green_offset)
        
        if self.blue_multiplier is not None:
            xml.attrib["blueMultiplier"] = str(self.blue_multiplier)
        
        if self.blue_offset is not None:
            xml.attrib["blueOffset"] = str(self.blue_offset)
        
        if self.alpha_multiplier is not None:
            xml.attrib["alphaMultiplier"] = str(self.alpha_multiplier)
        
        if self.alpha_offset is not None:
            xml.attrib["alphaOffset"] = str(self.alpha_offset)

        return xml
