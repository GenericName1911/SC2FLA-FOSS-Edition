import os

from lxml.etree import *
from shutil import rmtree

from PIL import Image

from .folder_item import DOMFolderItem
from .bitmap_item import DOMBitmapItem
from .symbol_item import DOMSymbolItem
from .timeline import DOMTimeline

from ..dat.bitmap import Bitmap

from . import NAMESPACES

from lib.console import Console

from datetime import datetime
from lib.fla.time import GetTime
from lib.utils import BinaryWriter

class folders(list):
    def __init__(self, library: str):
        self.library = library

    def add(self, folder_item):
        if isinstance(folder_item, DOMFolderItem):
            os.makedirs(os.path.join(self.library, folder_item.name), exist_ok=True)
            self.append(folder_item)

    def delete(self, index):
        object = self[index]
        rmtree(os.path.join(self.library, object.name))
        del self[index]

class symbols(dict):
    def __init__(self, library: str):
        self.library = library
        self.data = {}
        self.usage: dict[str, list[str]] = {}

    def add(self, key, value):
        path = os.path.join(self.library, str(key) + ".xml")
        value.save(path)

        self.data[key] = path

    def get(self, key):
        symbol = DOMSymbolItem()
        symbol.load(self.data[key])
        return symbol


class DOMDocument:
    def __init__(self, filepath: str) -> None:
        # class fields
        self.filepath = filepath

        # attributes
        self.xfl_version: float = 2.971
        self.creator_info: str = "Generated with XFL Python module by Pavel Sokov (GIHUB: github.com/Fred-31)"

        self.width: int = 1280
        self.height: int = 720
        self.frame_rate: int = 30

        self.current_timeline: int = 1
        self.background_color: int = 0x666666

        # elements
        self.folders = folders(self.librarypath)
        self.media: dict = {}
        self.symbols = symbols(self.librarypath)
        self.timelines: list = []

        if not os.path.exists(self.binarypath):
            os.mkdir(self.binarypath)

        if not os.path.exists(self.librarypath):
            os.mkdir(self.librarypath)
    
    @property
    def librarypath(self):
        path = f"{self.filepath}/LIBRARY"
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    
    @property
    def binarypath(self):
        path = f"{self.filepath}/bin"
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    
    def load(self):
        parsed = parse(os.path.join(self.filepath, "DOMDocument.xml"))
        xml = parsed.getroot()

        if "xflVersion" in xml.attrib:
            self.xfl_version = float(xml.attrib["xflVersion"])
        
        if "creatorInfo" in xml.attrib:
            self.creator_info = xml.attrib["creatorInfo"]
        
        if "width" in xml.attrib:
            self.width = int(xml.attrib["width"])
        
        if "height" in xml.attrib:
            self.height = int(xml.attrib["height"])
        
        if "frameRate" in xml.attrib:
            self.frame_rate = int(xml.attrib["frameRate"])
        
        if "currentTimeline" in xml.attrib:
            self.current_timeline = int(xml.attrib["currentTimeline"])
        
        if "backgroundColor" in xml.attrib:
            self.background_color = int(xml.attrib["backgroundColor"].replace("#", "0x"), 0)
        
        folders = xml.find("./xfl:folders", NAMESPACES)
        media = xml.find("./xfl:media", NAMESPACES)
        symbols = xml.find("./xfl:symbols", NAMESPACES)
        timelines = xml.find("./xfl:timelines", NAMESPACES)

        if folders is not None:
            for folder_element in folders:
                folder = DOMFolderItem()
                folder.load(folder_element)
                self.folders.append(folder)
        
        if media is not None:
            for media_element in media:
                bitmap = DOMBitmapItem()
                bitmap.load(media_element)

                if bitmap.bitmap_data_href is not None:
                    bitmap.image = Bitmap.load(os.path.join(self.binarypath, bitmap.bitmap_data_href))

                    # TODO: external source image loading
                    if bitmap.source_external_filepath is not None:
                        bitmap.image = Image.open(os.path.join(self.filepath, os.path.normpath(bitmap.source_external_filepath)))

                self.media[bitmap.name] = bitmap
        
        if symbols is not None:
            for symbol_element in symbols:
                symbol = DOMSymbolItem()
                symbol.load(os.path.join(self.librarypath, symbol_element.attrib["href"]))
                self.symbols[symbol.name] = os.path.join(self.librarypath, symbol_element.attrib["href"])
        
        if timelines is not None:
            for timeline_element in timelines:
                timeline = DOMTimeline()
                timeline.load(timeline_element)
                self.timelines.append(timeline)

    def save(self):
        for folder in self.folders:
            if folder.name is not None and folder.name != "":
                if not os.path.exists(os.path.join(self.librarypath, folder.name)):
                    os.mkdir(os.path.join(self.librarypath, folder.name))
        XSI = "http://www.w3.org/2001/XMLSchema-instance"
        xml = Element("DOMDocument", {"xmlns": NAMESPACES["xfl"]}, nsmap={'xsi': NAMESPACES["xsi"]})

        if self.xfl_version is not None:
            xml.attrib["xflVersion"] = str(self.xfl_version)
        
        if self.creator_info is not None and self.creator_info != "":
            xml.attrib["creatorInfo"] = str(self.creator_info)
        
        if self.width is not None:
            xml.attrib["width"] = str(self.width)
        
        if self.height is not None:
            xml.attrib["height"] = str(self.height)
        
        if self.frame_rate is not None:
            xml.attrib["frameRate"] = str(self.frame_rate)
        
        if self.current_timeline is not None:
            xml.attrib["currentTimeline"] = str(self.current_timeline)
        
        if self.background_color is not None:
            xml.attrib["backgroundColor"] = "#" + str(hex(self.background_color).lstrip("0x").zfill(6))
        
        folders = SubElement(xml, "folders")
        media = SubElement(xml, "media")
        symbols = SubElement(xml, "symbols")
        timelines = SubElement(xml, "timelines")
        
        for folder in self.folders:
            if folder.name is not None and folder.name != "":
                folders.append(folder.save())

        for i, media_name in enumerate(self.media):
            medium = self.media[media_name]
            media.append(medium.save())

            # TODO: external source image saving
            if medium.source_external_filepath is not None:
                medium.image.save(os.path.join(self.filepath, os.path.normpath(medium.source_external_filepath)), "PNG")

            if medium.image is not None:
                Bitmap.save(os.path.join(self.binarypath, medium.bitmap_data_href), medium.image)

            Console.progress_bar("Adobe binary images saving...", i, len(self.media))
        print()
        
        symbol_names: list[str] = list(self.symbols.data.keys())
        
        today_date = datetime.now()
        sys_cache = BinaryWriter()
        sys_cache.write_int(103)
        sys_cache.write_ushort(today_date.year)
        sys_cache.write_ushort(today_date.month)
        sys_cache.write_ushort(today_date.weekday())
        sys_cache.write_ushort(today_date.day)
        sys_cache.write_ushort(today_date.hour)
        sys_cache.write_ushort(today_date.minute)
        sys_cache.write_ushort(today_date.second)
        sys_cache.write_ushort(0)
        
        sys_cache.write_int(len(symbol_names))
        
        for name in symbol_names:
            sys_cache.write_ushort(len(name))
            sys_cache.write(bytes(name, 'utf-8'))
            
        sys_cache.write_int(44478)
        
        for name in symbol_names:
            usage_list = [] if name not in self.symbols.usage else self.symbols.usage[name]
            
            sys_cache.write_int(len(usage_list))
            for usage_item_name in usage_list:
                sys_cache.write_int(symbol_names.index(usage_item_name))
                
        with open(os.path.join(self.binarypath, "SymDepend.cache"), 'wb') as file:
            file.write(sys_cache.buffer)
        
        for i in range(len(symbol_names)):
            symbol = self.symbols.get(symbol_names[i]) # Too expensive
            

            include = Element("Include")
            include.attrib["loadImmediate"] = "false"
            include.attrib["href"] = symbol_names[i] + ".xml"
            include.attrib["itemID"] = f"{int((symbol.creationDate - datetime(1970, 1, 1)).total_seconds()):08x}-{i+290:08x}"
            include.attrib["lastModified"] = str(int((GetTime() - datetime(1970, 1, 1)).total_seconds()))

            symbols.append(include)

        for timeline in self.timelines:
            timelines.append(timeline.save())

        ElementTree(xml).write(os.path.join(self.filepath, "DOMDocument.xml"), pretty_print=True)
        
        with open(os.path.join(self.filepath, os.path.basename(self.filepath) + ".xfl"), 'w') as file:
            file.write("PROXY-CS5")
