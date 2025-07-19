from lxml.etree import *
from ..geom.matrix import Matrix

from ..dom import NAMESPACES


class BitmapFill:
    def __init__(self, path: str = None) -> None:
        # attributes
        self.path = path
        self.matrix: Matrix = None

    def load(self, xml: Element):
        if "bitmapPath" in xml.attrib:
            self.path = xml.attrib["bitmapPath"]

        matrix = xml.find("./xfl:matrix", NAMESPACES)
        if matrix is not None:
            for matrix_element in matrix:
                self.matrix = Matrix()
                self.matrix.load(matrix_element)

    def save(self):
        xml = Element("BitmapFill")

        if self.path is not None:
            xml.attrib["bitmapPath"] = str(self.path)

        if self.matrix is not None:
            matrix = SubElement(xml, "matrix")
            matrix.append(self.matrix.save())

        return xml
