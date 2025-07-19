from lxml.etree import *

from ..edge.edge import Edge
from ..fill.fill_style import FillStyle
from ..stroke.stroke_style import StrokeStyle

from ..geom.matrix import Matrix

from . import NAMESPACES


class DOMShape:
    def __init__(self) -> None:
        # attributes
        self.is_drawing_object: bool = False

        # elements
        self.edges: list = []
        self.fills: list = []
        self.strokes: list = []
        self.matrix: Matrix = None
    
    def load(self, xml: Element):
        if "isDrawingObject" in xml.attrib:
            self.is_drawing_object = xml.attrib["isDrawingObject"] == "true"

        fills = xml.find("./xfl:fills", NAMESPACES)
        strokes = xml.find("./xfl:strokes", NAMESPACES)
        edges = xml.find("./xfl:edges", NAMESPACES)

        matrix = xml.find("./xfl:matrix", NAMESPACES)
        if matrix is not None:
            for matrix_element in matrix:
                self.matrix = Matrix()
                self.matrix.load(matrix_element)

        if fills is not None:
            for fill_element in fills:
                fill = FillStyle()
                fill.load(fill_element)
                self.fills.append(fill)
        
        if strokes is not None:
            for stroke_element in strokes:
                stroke = StrokeStyle()
                stroke.load(stroke_element)
                self.strokes.append(stroke)
        
        if edges is not None:
            for edge_element in edges:
                edge = Edge()
                edge.load(edge_element)

                if edge.edges is not None and edge.edges != "":
                    self.edges.append(edge)
    
    def save(self):
        xml = Element("DOMShape")

        if self.is_drawing_object:
            xml.attrib["isDrawingObject"] = str(self.is_drawing_object).lower()

        fills = SubElement(xml, "fills")
        strokes = SubElement(xml, "strokes")
        edges = SubElement(xml, "edges")

        if self.matrix is not None:
            matrix = SubElement(xml, "matrix")
            matrix.append(self.matrix.save())

        for fill in self.fills:
            fills.append(fill.save())
        
        for stroke in self.strokes:
            strokes.append(stroke.save())
        
        for edge in self.edges:
            edges.append(edge.save())

        return xml
