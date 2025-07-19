from lxml.etree import *

from .gradient_entry import GradientEntry
from ..geom.matrix import Matrix

from ..dom import NAMESPACES


class LinearGradient:
    def __init__(self, spread_method: str = None) -> None:
        # attributes
        self.spread_method = spread_method

        # elements
        self.matrix: Matrix = None
        self.entries: list = []
    
    def load(self, xml: Element):
        if "spreadMethod" in xml.attrib:
            self.spread_method = xml.attrib["spreadMethod"]
        
        matrix = xml.find("./xfl:matrix", NAMESPACES)
        if matrix is not None:
            for matrix_element in matrix:
                self.matrix = Matrix()
                self.matrix.load(matrix_element)
        
        entries = xml.findall("./xfl:GradientEntry", NAMESPACES)
        for entrie_element in entries:
            entrie = GradientEntry()
            entrie.load(entrie_element)
            self.entries.append(entrie)
    
    def save(self):
        xml = Element("LinearGradient")

        if self.spread_method is not None:
            xml.attrib["spreadMethod"] = str(self.spread_method)
        
        if self.matrix is not None:
            matrix = SubElement(xml, "matrix")
            matrix.append(self.matrix.save())
        
        for entrie in self.entries:
            xml.append(entrie.save())

        return xml
