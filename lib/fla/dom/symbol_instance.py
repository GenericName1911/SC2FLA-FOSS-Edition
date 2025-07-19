from lxml.etree import *

from ..geom.matrix import Matrix
from ..geom.color import Color
from ..geom.point import Point

from . import NAMESPACES


class DOMSymbolInstance:
    def __init__(self, name: str = None, library_item_name: str = None, loop: str = None) -> None:
        # attributes
        self.name = name
        self.library_item_name = library_item_name
        self.blend_mode: str = None
        self.type: str = None

        self.loop = loop

        # elements
        self.matrix: Matrix = None
        self.color: Color = None
        self.transformation_point: Point = None
    
    def load(self, xml: Element):
        if "name" in xml.attrib:
            self.name = xml.attrib["name"]
        
        if "libraryItemName" in xml.attrib:
            self.library_item_name = xml.attrib["libraryItemName"]

        if "blendMode" in xml.attrib:
            self.blend_mode = xml.attrib["blendMode"]
        
        if "loop" in xml.attrib:
            self.loop = xml.attrib["loop"]

        if "symbolType" in xml.attrib:
            self.type = xml.attrib["symbolType"]

        matrix = xml.find("./xfl:matrix", NAMESPACES)
        if matrix is not None:
            for matrix_element in matrix:
                self.matrix = Matrix()
                self.matrix.load(matrix_element)
        
        color = xml.find("./xfl:color", NAMESPACES)
        if color is not None:
            for color_element in color:
                self.color = Color()
                self.color.load(color_element)
        
        transformation_point = xml.find("./xfl:transformationPoint", NAMESPACES)
        if transformation_point is not None:
            for point_element in transformation_point:
                self.transformation_point = Point()
                self.transformation_point.load(point_element)
    
    def save(self):
        xml = Element("DOMSymbolInstance")

        if self.name is not None:
            xml.attrib["name"] = str(self.name)

        if self.library_item_name is not None:
            xml.attrib["libraryItemName"] = str(self.library_item_name)

        if self.blend_mode is not None:
            xml.attrib["blendMode"] = str(self.blend_mode)
        
        if self.loop is not None:
            xml.attrib["loop"] = str(self.loop)

        if self.type is not None:
            xml.attrib["symbolType"] = str(self.type)
        
        if self.matrix is not None:
            matrix = SubElement(xml, "matrix")
            matrix.append(self.matrix.save())

        if self.color is not None:
            color = SubElement(xml, "color")
            color.append(self.color.save())

        if self.transformation_point is not None:
            transformation_point = SubElement(xml, "transformationPoint")
            transformation_point.append(self.transformation_point.save())

        return xml
