from lxml.etree import *

from . import NAMESPACES
from .frame import DOMFrame


class DOMLayer:
    def __init__(self, name: str = None, auto_named: bool = None, color: int = None, layer_type: str = None, parent_layer_index: int = None, current: bool = None) -> None:
        # attributes
        self.name = name
        self.auto_named = auto_named

        self.color = color

        self.layer_type = layer_type
        self.parent_layer_index = parent_layer_index

        self.current = current
        self.is_selected: bool = None
        self.is_locked: bool = None

        self.animation_type: str = None

        # elements
        self.frames: list = []
    
    def load(self, xml: Element):
        if "name" in xml.attrib:
            self.name = xml.attrib["name"]
        
        if "autoNamed" in xml.attrib:
            self.auto_named = xml.attrib["autoNamed"] == "true"
        
        if "color" in xml.attrib:
            self.color = int(xml.attrib["color"].replace("#", "0x"), 0)
        
        if "layerType" in xml.attrib:
            self.layer_type = xml.attrib["layerType"]
        
        if "parentLayerIndex" in xml.attrib:
            self.parent_layer_index = int(xml.attrib["parentLayerIndex"])
        
        if "current" in xml.attrib:
            self.current = xml.attrib["current"] == "true"
        
        if "isSelected" in xml.attrib:
            self.is_selected = xml.attrib["isSelected"] == "true"
        
        if "locked" in xml.attrib:
            self.is_locked = xml.attrib["locked"] == "true"
        
        if "animationType" in xml.attrib:
            self.animation_type = xml.attrib["animationType"]
        
        frames = xml.find("./xfl:frames", NAMESPACES)
        if frames is not None:
            for frame_element in frames:
                frame = DOMFrame()
                frame.load(frame_element)
                self.frames.append(frame)
    
    def save(self):
        xml = Element("DOMLayer")

        if self.name is not None:
            xml.attrib["name"] = str(self.name)
        
        if self.auto_named is not None:
            xml.attrib["autoNamed"] = "true" if self.auto_named else "false"
        
        if self.color is not None:
            xml.attrib["color"] = "#" + str(hex(self.color).lstrip("0x").zfill(6))
        
        if self.layer_type is not None:
            xml.attrib["layerType"] = str(self.layer_type)
        
        if self.parent_layer_index is not None:
            xml.attrib["parentLayerIndex"] = str(self.parent_layer_index)
        
        if self.current is not None:
            xml.attrib["current"] = "true" if self.current else "false"
        
        if self.is_selected is not None:
            xml.attrib["isSelected"] = "true" if self.is_selected else "false"

        if self.is_locked is not None:
            xml.attrib["locked"] = "true" if self.is_locked else "false"
        
        if self.animation_type is not None:
            xml.attrib["animationType"] = str(self.animation_type)
        
        frames = SubElement(xml, "frames")
        for frame in self.frames:
            frames.append(frame.save())

        return xml
