from lxml.etree import *

from .text_run import DOMTextRun

from ..filter.glow_filter import GlowFilter
from ..filter.drop_shadow_filter import DrowShadowFilter

from ..geom.matrix import Matrix
from ..geom.color import Color

from . import NAMESPACES


class DOMStaticText:
    def __init__(self) -> None:
        # attributes
        self.width: float = None
        self.height: float = None

        self.is_selectable: bool = None

        # elements
        self.text_runs: list = []
        
        self.filters: list = []

        self.matrix: Matrix = None
        self.color: Color = None
    
    def load(self, xml: Element):
        if "width" in xml.attrib:
            self.width = float(xml.attrib["width"])
        
        if "height" in xml.attrib:
            self.height = float(xml.attrib["height"])
        
        if "isSelectable" in xml.attrib:
            self.is_selectable = xml.attrib["isSelectable"] == "true"
        
        text_runs = xml.find("./xfl:textRuns", NAMESPACES)
        if text_runs is not None:
            for text_run_element in text_runs:
                text_run = DOMTextRun()
                text_run.load(text_run_element)
                self.text_runs.append(text_run)
        
        filters = xml.find("./xfl:filters", NAMESPACES)
        if filters is not None:
            for filter in filters:
                if filter.tag.startswith("GlowFilter"):
                    glow_filter = GlowFilter()
                    glow_filter.load(filter)
                    self.filters.append(glow_filter)
                
                elif filter.tag.startswith("DrowShadowFilter"):
                    shadow_filter = DrowShadowFilter()
                    shadow_filter.load(filter)
                    self.filters.append(shadow_filter)
        
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
    
    def save(self):
        xml = Element("DOMStaticText")

        if self.width is not None:
            xml.attrib["width"] = str(self.width)
        
        if self.height is not None:
            xml.attrib["height"] = str(self.height)
        
        if self.is_selectable is not None:
            xml.attrib["isSelectable"] = "true" if self.is_selectable else "false"
        
        text_runs = SubElement(xml, "textRuns")
        for text_run in self.text_runs:
            text_runs.append(text_run.save())
        
        if self.filters:
            filters = SubElement(xml, "filters")
            for filter in self.filters:
                filters.append(filter.save())

        if self.matrix is not None:
            matrix = SubElement(xml, "matrix")
            matrix.append(self.matrix.save())

        if self.color is not None:
            color = SubElement(xml, "color")
            color.append(self.color.save())

        return xml
