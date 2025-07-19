from lxml.etree import *

from . import NAMESPACES
from .layer import DOMLayer


class DOMTimeline:
    def __init__(self, name: str = None) -> None:
        # attributes
        self.name = name

        # elements
        self.layers: list = []
    
    def load(self, xml: Element):
        if "name" in xml.attrib:
            self.name = xml.attrib["name"]
        
        layers = xml.find("./xfl:layers", NAMESPACES)
        if layers is not None:
            for layer_element in layers:
                layer = DOMLayer()
                layer.load(layer_element)
                self.layers.append(layer)
    
    def save(self):
        xml = Element("DOMTimeline")

        if self.name is not None:
            xml.attrib["name"] = str(self.name)
        
        layers = SubElement(xml, "layers")
        for layer in self.layers:
            layers.append(layer.save())

        return xml
