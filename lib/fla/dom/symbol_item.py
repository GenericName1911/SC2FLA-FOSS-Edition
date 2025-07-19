from lxml.etree import *

from . import NAMESPACES
from .timeline import DOMTimeline

from lib.fla.time import GetTime

from io import StringIO

class DOMSymbolItem:
    def __init__(self, name: str = None, symbol_type: str = None) -> None:
        # attributes
        self.name = name
        self.item_id: str = None
        self.symbol_type = symbol_type

        self.scale_grid_left: float = None
        self.scale_grid_top: float = None
        self.scale_grid_right: float = None
        self.scale_grid_bottom: float = None

        # elements
        self.timeline: DOMTimeline = DOMTimeline()

        self.creationDate = GetTime()
    
    def load(self, filepath: str):
        xml = fromstring(open(filepath, "r").read())
        
        if "name" in xml.attrib:
            self.name = xml.attrib["name"]
        
        if "itemID" in xml.attrib:
            self.item_id = xml.attrib["itemID"]
        
        if "symbolType" in xml.attrib:
            self.symbol_type = xml.attrib["symbolType"]
        
        if "scaleGridLeft" in xml.attrib:
            self.scale_grid_left = float(xml.attrib["scaleGridLeft"])
        
        if "scaleGridTop" in xml.attrib:
            self.scale_grid_top = float(xml.attrib["scaleGridTop"])
        
        if "scaleGridRight" in xml.attrib:
            self.scale_grid_right = float(xml.attrib["scaleGridRight"])
        
        if "scaleGridBottom" in xml.attrib:
            self.scale_grid_bottom = float(xml.attrib["scaleGridBottom"])
        
        timelines = xml.find("./xfl:timeline", NAMESPACES)
        if timelines is not None:
            for timeline in timelines:
                self.timeline = DOMTimeline()
                self.timeline.load(timeline)
    
    def save(self, filepath: str):
        xml = Element("DOMSymbolItem", {"xmlns": NAMESPACES["xfl"]}, nsmap={'xsi': NAMESPACES["xsi"]})

        if self.name is not None:
            xml.attrib["name"] = str(self.name)
        
        if self.item_id is not None:
            xml.attrib["itemID"] = str(self.item_id)
        
        if self.symbol_type is not None:
            xml.attrib["symbolType"] = str(self.symbol_type)
        
        if self.scale_grid_left is not None:
            xml.attrib["scaleGridLeft"] = str(self.scale_grid_left)
        
        if self.scale_grid_top is not None:
            xml.attrib["scaleGridTop"] = str(self.scale_grid_top)
        
        if self.scale_grid_right is not None:
            xml.attrib["scaleGridRight"] = str(self.scale_grid_right)
        
        if self.scale_grid_bottom is not None:
            xml.attrib["scaleGridBottom"] = str(self.scale_grid_bottom)

        timeline = SubElement(xml, "timeline")
        if self.timeline is not None:
            timeline.append(self.timeline.save())


        open(filepath, "wb").write(tostring(xml, encoding='utf8'))
