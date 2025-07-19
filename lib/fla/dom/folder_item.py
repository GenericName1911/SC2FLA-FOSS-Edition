from lxml.etree import *


class DOMFolderItem:
    def __init__(self, name: str = None) -> None:
        # attributes
        self.name = name
        self.item_id: str = None
        self.is_expanded: bool = False
    
    def load(self, xml: Element):
        if "name" in xml.attrib:
            self.name = xml.attrib["name"]
        
        if "itemID" in xml.attrib:
            self.item_id = xml.attrib["itemID"]
        
        if "isExpanded" in xml.attrib:
            self.is_expanded = xml.attrib["isExpanded"] == "true"
    
    def save(self):
        xml = Element("DOMFolderItem")

        if self.name is not None:
            xml.attrib["name"] = str(self.name)
        
        if self.item_id is not None:
            xml.attrib["itemID"] = str(self.item_id)
        
        if self.is_expanded is not None:
            xml.attrib["isExpanded"] = "true" if self.is_expanded else "false"
        
        return xml
