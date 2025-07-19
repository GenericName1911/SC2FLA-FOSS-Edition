from lxml.etree import *


class DOMTextAttrs:
    def __init__(self) -> None:
        # attributes
        self.face: str = None

        self.size: float = 0
        self.bitmap_size: int = 0

        self.left_margin: float = 0
        self.right_margin: float = 0

        self.indent: float = 0.0
        self.line_spacing: float = 0.0
        self.letter_spacing: int = 0
        self.line_height: float = 0.0

        self.alias_text: bool = False
        self.auto_kern: bool = True

        self.alignment: str = None

        self.fill_color: int = 0x000000
        self.alpha: float = 1
    
    def load(self, xml: Element):
        if "face" in xml.attrib:
            self.face = xml.attrib["face"]
        
        if "size" in xml.attrib:
            self.size = float(xml.attrib["size"])
        
        if "bitmapSize" in xml.attrib:
            self.bitmap_size = int(xml.attrib["bitmapSize"])
        
        if "leftMargin" in xml.attrib:
            self.left_margin = float(xml.attrib["leftMargin"])
        
        if "rightMargin" in xml.attrib:
            self.right_margin = float(xml.attrib["rightMargin"])
        
        if "aliasText" in xml.attrib:
            self.alias_text = xml.attrib["aliasText"] == "true"
        
        if "alignment" in xml.attrib:
            self.alignment = xml.attrib["alignment"]
        
        if "fillColor" in xml.attrib:
            self.fill_color = int(xml.attrib["fillColor"].replace("#", "0x"), 0)
        
        if "alpha" in xml.attrib:
            self.alpha = float(xml.attrib["alpha"])
    def save(self):
        xml = Element("DOMTextAttrs")

        if self.face is not None and self.face != "":
            xml.attrib["face"] = str(self.face)
        
        if self.size is not None:
            xml.attrib["size"] = str(self.size)
        
        if self.bitmap_size is not None:
            xml.attrib["bitmapSize"] = str(self.bitmap_size)
        
        if self.left_margin is not None:
            xml.attrib["leftMargin"] = str(self.left_margin)
        
        if self.right_margin is not None:
            xml.attrib["rightMargin"] = str(self.right_margin)
        
        if self.alias_text is not None:
            xml.attrib["aliasText"] = "true" if self.alias_text else "false"
        
        if self.alignment is not None:
            xml.attrib["alignment"] = str(self.alignment)
        
        if self.fill_color is not None:
            xml.attrib["fillColor"] = hex(self.fill_color).replace("0x", "#")[:7]
        
        if self.alpha is not None:
            xml.attrib["alpha"] = str(self.alpha)

        return xml
