from lxml.etree import *

from .bitmap_instance import DOMBitmapInstance
from .symbol_instance import DOMSymbolInstance
from .shape import DOMShape
from .static_text import DOMStaticText
from .dynamic_text import DOMDynamicText

from ..geom.matrix import Matrix

from . import NAMESPACES


class DOMGroup:
    def __init__(self):
        # elements
        self.members: list = []
        self.matrix: Matrix = None

    def load(self, xml: Element):
        matrix = xml.find("./xfl:matrix", NAMESPACES)
        if matrix is not None:
            for matrix_element in matrix:
                self.matrix = Matrix()
                self.matrix.load(matrix_element)
        
        for member in xml.find("./xfl:members", NAMESPACES):
            if member.tag.endswith("DOMBitmapInstance"):
                    bitmap_instance = DOMBitmapInstance()
                    bitmap_instance.load(member)
                    self.members.append(bitmap_instance)
                
            elif member.tag.endswith("DOMSymbolInstance"):
                symbol_instance = DOMSymbolInstance()
                symbol_instance.load(member)
                self.members.append(symbol_instance)
            
            elif member.tag.endswith("DOMShape"):
                shape = DOMShape()
                shape.load(member)
                self.members.append(shape)
            
            elif member.tag.endswith("DOMStaticText"):
                static_text = DOMStaticText()
                static_text.load(member)
                self.members.append(static_text)
            
            elif member.tag.endswith("DOMDynamicText"):
                dynamic_text = DOMDynamicText()
                dynamic_text.load(member)
                self.members.append(dynamic_text)

            elif member.tag.endswith("DOMGroup"):
                group = DOMGroup()
                group.load(member)
                self.members.append(group)

    def save(self):
        xml = Element("DOMGroup")

        if self.matrix is not None:
            matrix = SubElement(xml, "matrix")
            matrix.append(self.matrix.save())

        members = SubElement(xml, "members")
        for member in self.members:
            members.append(member.save())

        return xml
