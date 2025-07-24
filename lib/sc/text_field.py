from io import BytesIO
from .writable import Writable

class TextField(Writable):
    def __init__(self) -> None:
        super().__init__()

        self.font_name: str = "none"
        self.font_color: int = 0xFFFFFF
        self.outline_color: int = 0xFFFFFF
        self.font_size: int = 0
        self.font_align: int = 0

        self.bold: bool = False
        self.italic: bool = False
        self.multiline: bool = False
        self.outline: bool = False

        self.left_corner: int = 0
        self.top_corner: int = 0
        self.right_corner: int = 0
        self.bottom_corner: int = 0

        self.text: str = None
        self.isDynamic: bool = False

        self.flag1: bool = None
        self.flag2: bool = None
        self.flag3: bool = None

        self.c1: int = None
        self.c2: int = None

    def load(self, swf, tag: int):
        id = swf.reader.read_ushort()
        
        self.font_name = swf.reader.read_ascii() or "none"
        swf.reader.read_int()
        self.font_color = 0xFFFFFF

        self.bold = swf.reader.read_bool()
        self.italic = swf.reader.read_bool()
        self.multiline = swf.reader.read_bool()
        self.isDynamic = swf.reader.read_bool()

        self.font_align = swf.reader.read_uchar()
        self.font_size = swf.reader.read_uchar()

        self.top_corner = swf.reader.read_short()
        self.bottom_corner = swf.reader.read_short()
        self.left_corner = swf.reader.read_short()
        self.right_corner = swf.reader.read_short()

        self.outline = swf.reader.read_bool()
        self.text = swf.reader.read_ascii()

        if tag == 7:
            return id

        self.flag1 = swf.reader.read_bool()

        if tag > 15:
            self.flag2 = tag != 25

        if tag > 20:
            self.outline_color = swf.reader.read_int()

        if tag > 25:
            self.c1 = swf.reader.read_short()
            swf.reader.read_short()

        if tag > 33:
            self.c2 = swf.reader.read_short()

        if tag > 43:
            self.flag3 = swf.reader.read_bool()

        if tag > 44:
            print(swf.reader.read_ascii())

        return id

    def save(self, id: int):
        super().save()

        tag = 7

        self.write_ushort(id)

        self.write_ascii(self.font_name)
        self.write_int(self.font_color)

        self.write_bool(self.bold)
        self.write_bool(self.italic)
        self.write_bool(self.multiline)
        self.write_bool(False)

        self.write_uchar(self.font_align)
        self.write_uchar(self.font_size)

        self.write_short(self.top_corner)
        self.write_short(self.bottom_corner)
        self.write_short(self.left_corner)
        self.write_short(self.right_corner)

        self.write_bool(self.outline)
        self.write_ascii(self.text)

        if self.flag1 is not None:
            tag = 15
            self.write_bool(self.flag1)

            if self.flag2 is not None:
                if self.flag2:
                    tag = 20
                else:
                    if self.outline_color is not None:
                        tag = 21
                        self.write_int(self.outline_color)

                        if self.c1 is not None:
                            tag = 25
                            self.write_short(self.c1)
                            self.write_short(0)

                            if self.c2 is not None:
                                tag = 33
                                self.write_short(self.c2)

                                if self.flag3 is not None:
                                    tag = 43
                                    if self.flag3:
                                        tag = 44
                                        self.write_bool(self.flag3)

        return tag, self.buffer

    def __eq__(a, b):
        if type(a) == type(b):
            if a.font_name == b.font_name\
                    and a.font_color == b.font_color\
                    and a.outline_color == b.outline_color\
                    and a.font_size == b.font_size\
                    and a.font_align == b.font_align\
                    and a.bold == b.bold\
                    and a.italic == b.italic\
                    and a.multiline == b.multiline\
                    and a.left_corner == b.left_corner\
                    and a.top_corner == b.top_corner\
                    and a.right_corner == b.right_corner\
                    and a.bottom_corner == b.bottom_corner\
                    and a.text == b.text\
                    and a.flag1 == b.flag1\
                    and a.flag2 == b.flag2\
                    and a.flag3 == b.flag3\
                    and a.c1 == b.c1\
                    and a.c2 == b.c2:
                return True
        return False
