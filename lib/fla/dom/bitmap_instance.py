from lxml.etree import *

from ..geom.matrix import Matrix
from ..geom.color import Color
from ..geom.point import Point

from . import NAMESPACES


class DOMBitmapInstance:
    def __init__(self, library_item_name: str = None) -> None:
        # attributes
        self.name: str = None
        self.library_item_name = library_item_name

        # elements
        self.matrix: Matrix = None
        self.transformation_point: Point = None
    
    def load(self, xml: Element):
        if "name" in xml.attrib:
            self.name = xml.attrib["name"]

        if "libraryItemName" in xml.attrib:
            self.library_item_name = xml.attrib["libraryItemName"]
        
        matrix = xml.find("./xfl:matrix", NAMESPACES)
        if matrix is not None:
            for matrix_element in matrix:
                self.matrix = Matrix()
                self.matrix.load(matrix_element)
        
        transformation_point = xml.find("./xfl:transformationPoint", NAMESPACES)
        if transformation_point is not None:
            for point_element in transformation_point:
                self.transformation_point = Point()
                self.transformation_point.load(point_element)
    
    def save(self):
        xml = Element("DOMBitmapInstance")

        if self.name is not None:
            xml.attrib["name"] = str(self.name)

        if self.library_item_name is not None:
            xml.attrib["libraryItemName"] = str(self.library_item_name)
        
        if self.matrix is not None:
            matrix = SubElement(xml, "matrix")
            matrix.append(self.matrix.save())

        if self.transformation_point is not None:
            transformation_point = SubElement(xml, "transformationPoint")
            transformation_point.append(self.transformation_point.save())

        return xml
