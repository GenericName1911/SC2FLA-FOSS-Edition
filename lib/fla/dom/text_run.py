from lxml.etree import *

from .text_attrs import DOMTextAttrs

from . import NAMESPACES


class DOMTextRun:
    def __init__(self, characters: str = None) -> None:
        # elements
        self.characters = characters
        self.text_attrs: list = []
    
    def load(self, xml: Element):
        characters = xml.find("./xfl:characters", NAMESPACES)
        if characters is not None:
            self.characters = characters.text
        
        text_attrs = xml.find("./xfl:textAttrs", NAMESPACES)
        if text_attrs is not None:
            for text_attr_element in text_attrs:
                text_attr = DOMTextAttrs()
                text_attr.load(text_attr_element)
                self.text_attrs.append(text_attr)
    
    def save(self):
        xml = Element("DOMTextRun")

        if self.characters is not None and self.characters != "":
            SubElement(xml, "characters").text = str(self.characters)
        
        text_attrs = SubElement(xml, "textAttrs")
        for text_attr in self.text_attrs:
            text_attrs.append(text_attr.save())

        return xml
