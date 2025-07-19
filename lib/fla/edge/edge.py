from lxml.etree import *


class Edge:
    def __init__(self) -> None:
        # attributes
        self.edges: str = None # TODO: abstract it to draw commands
        self.fill_style0: int = None
        self.fill_style1: int = None
        self.stroke_style: int = None
    
    def load(self, xml: Element):
        if "edges" in xml.attrib:
            self.edges = xml.attrib["edges"]
        
        if "fillStyle0" in xml.attrib:
            self.fill_style0 = int(xml.attrib["fillStyle0"])
        
        if "fillStyle1" in xml.attrib:
            self.fill_style1 = int(xml.attrib["fillStyle1"])
        
        if "strokeStyle" in xml.attrib:
            self.stroke_style = int(xml.attrib["strokeStyle"])
    
    def save(self):
        xml = Element("Edge")

        if self.edges is not None and self.edges != "":
            xml.attrib["edges"] = str(self.edges)
        
        if self.fill_style0 is not None:
            xml.attrib["fillStyle0"] = str(self.fill_style0)
        
        if self.fill_style1 is not None:
            xml.attrib["fillStyle1"] = str(self.fill_style1)
        
        if self.stroke_style is not None:
            xml.attrib["strokeStyle"] = str(self.stroke_style)

        return xml
