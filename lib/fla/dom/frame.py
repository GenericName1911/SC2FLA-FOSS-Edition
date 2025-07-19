from lxml.etree import *

from enum import Enum

from . import NAMESPACES

from .bitmap_instance import DOMBitmapInstance
from .symbol_instance import DOMSymbolInstance
from .shape import DOMShape
from .group import DOMGroup
from .static_text import DOMStaticText
from .dynamic_text import DOMDynamicText
from ..geom.color import Color


class KeyMode(Enum):
    KEY_MODE_NORMAL = 9728
    KEY_MODE_CLASSIC_TWEEN = 22017
    KEY_MODE_SHAPE_TWEEN = 17922
    KEY_MODE_MOTION_TWEEN = 8195
    KEY_MODE_SHAPE_LAYERS = 8192


class DOMFrame:
    def __init__(self, index: int = None, duration: int = 1, name: str = None, label_type: str = None, key_mode: int = None) -> None:
        # attributes
        self.name = name
        self.label_type = label_type

        self.index = index
        self.duration = duration

        self.key_mode = key_mode
        self.blend_mode: str = None

        self.tween_type: str = None

        # self.motion_object = None # TODO: motion objects and tweens

        # elements
        self.elements: list = []
        self.script: str = None

        self.frame_color: Color = None
    
    def load(self, xml: Element):
        if "name" in xml.attrib:
            self.name = xml.attrib["name"]
        
        if "labelType" in xml.attrib:
            self.label_type = xml.attrib["labelType"]
        
        if "index" in xml.attrib:
            self.index = int(xml.attrib["index"])
        
        if "duration" in xml.attrib:
            self.duration = int(xml.attrib["duration"])
        
        if "keyMode" in xml.attrib:
            self.key_mode = int(xml.attrib["keyMode"])
        
        if "blendMode" in xml.attrib:
            self.blend_mode = xml.attrib["blendMode"]
        
        if "tweenType" in xml.attrib:
            self.tween_type = xml.attrib["tweenType"]

        script = xml.find("./xfl:Actionscript", NAMESPACES)

        if script is not None:
            for element in script:
                if element.tag == "script":
                    if str(element.text).startswith("![CDATA["):
                        self.script = element.text[7:len(element.text) - 2]

        elements = xml.find("./xfl:elements", NAMESPACES)

        if elements is not None:
            for element in elements:
                if element.tag.endswith("DOMBitmapInstance"):
                    bitmap_instance = DOMBitmapInstance()
                    bitmap_instance.load(element)
                    self.elements.append(bitmap_instance)
                
                elif element.tag.endswith("DOMSymbolInstance"):
                    symbol_instance = DOMSymbolInstance()
                    symbol_instance.load(element)
                    self.elements.append(symbol_instance)
                
                elif element.tag.endswith("DOMShape"):
                    shape = DOMShape()
                    shape.load(element)
                    self.elements.append(shape)
                
                elif element.tag.endswith("DOMStaticText"):
                    static_text = DOMStaticText()
                    static_text.load(element)
                    self.elements.append(static_text)
                
                elif element.tag.endswith("DOMDynamicText"):
                    dynamic_text = DOMDynamicText()
                    dynamic_text.load(element)
                    self.elements.append(dynamic_text)

                elif element.tag.endswith("DOMGroup"):
                    group = DOMGroup()
                    group.load(element)
                    self.elements.append(group)

        self.frame_color = xml.find("./xfl:frameColor", NAMESPACES)
        if self.frame_color is not None:
            for color_element in self.frame_color:
                self.color = Color()
                self.color.load(color_element)
    
    def save(self):
        xml = Element("DOMFrame")

        if self.name is not None:
            xml.attrib["name"] = str(self.name)
        
        if self.label_type is not None:
            xml.attrib["labelType"] = str(self.label_type)
        
        if self.index is not None:
            xml.attrib["index"] = str(self.index)
        
        if self.duration != 1:
            xml.attrib["duration"] = str(self.duration)
        
        if self.key_mode is not None:
            xml.attrib["keyMode"] = str(self.key_mode)
        
        if self.blend_mode is not None:
            xml.attrib["blendMode"] = str(self.blend_mode)
        
        if self.tween_type is not None:
            xml.attrib["tweenType"] = str(self.tween_type)

        if self.script is not None:
            action_script = SubElement(xml, "Actionscript")
            script = SubElement(action_script, "script")
            script.text = self.script
        
        elements = SubElement(xml, "elements")
        for element in self.elements:
            elements.append(element.save())

        return xml