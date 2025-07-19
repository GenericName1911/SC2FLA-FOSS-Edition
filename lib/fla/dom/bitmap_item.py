from lxml.etree import *

from PIL import Image

from datetime import datetime
from lib.fla.time import GetTime

class DOMBitmapItem:
    def __init__(self, name: str = None, bitmap_data_href: str = None) -> None:
        self.image: Image = None

        # attributes
        self.name = name
        self.bitmap_data_href = bitmap_data_href
        self.source_external_filepath: str = None
        self.quality: int = None
        self.use_imported_jpeg_data: bool = None
        self.compression_type: str = None
        self.allow_smoothing: bool = True
    
    def load(self, xml: Element):
        if "name" in xml.attrib:
            self.name = xml.attrib["name"]
        
        if "bitmapDataHRef" in xml.attrib:
            self.bitmap_data_href = xml.attrib["bitmapDataHRef"]
        
        if "sourceExternalFilepath" in xml.attrib:
            self.source_external_filepath = xml.attrib["sourceExternalFilepath"]
        
        if "quality" in xml.attrib:
            self.quality = xml.attrib["quality"]
        
        if "useImportedJPEGData" in xml.attrib:
            self.use_imported_jpeg_data = xml.attrib["useImportedJPEGData"] == "true"
        
        if "compressionType" in xml.attrib:
            self.compression_type = xml.attrib["compressionType"]
        
        if "allowSmoothing" in xml.attrib:
            self.allow_smoothing = xml.attrib["allowSmoothing"] == "true"
    
    def save(self):
        xml = Element("DOMBitmapItem")

        if self.name is not None:
            xml.attrib["name"] = str(self.name)
        
        if self.bitmap_data_href is not None:
            xml.attrib["bitmapDataHRef"] = str(self.bitmap_data_href)
        
        if self.source_external_filepath is not None:
            xml.attrib["sourceExternalFilepath"] = str(self.source_external_filepath)
        
        if self.quality is not None:
            xml.attrib["quality"] = str(self.quality)
        
        if self.use_imported_jpeg_data is not None:
            xml.attrib["useImportedJPEGData"] = "true" if self.use_imported_jpeg_data else "false"
        
        if self.compression_type is not None:
            xml.attrib["compressionType"] = str(self.compression_type)
        
        if self.allow_smoothing:
            xml.attrib["allowSmoothing"] = "true" if self.allow_smoothing else "false"

        xml.attrib["lastModified"] = str(int((GetTime() - datetime(1970, 1, 1)).total_seconds()))
        
        return xml
