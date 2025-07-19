from enum import Enum

from lib.console import Console

from .writable import Writable


# all blend modes used in Supercell games
BLENDMODES = [
    None,  # "mix" by default
    None,  # something like "mix" + "multiply"
    None,  # "layer"
    "multiply",
    "screen",
    None,  # "lighten"
    None,  # "darken"
    None,  # "difference"
    "add"
]


class Modifier(Enum):
    Mask = 38
    Masked = 39
    Unmasked = 40


class MovieClipModifier(Writable):
    def __init__(self) -> None:
        super().__init__()

        self.modifier: Modifier = Modifier.Mask

    def load(self, swf, tag: int):
        self.modifier = Modifier(tag)

        return swf.reader.read_ushort()

    def save(self, id: int):
        super().save()

        self.write_ushort(id)

        tag = self.modifier.value

        return tag, self.buffer

    def __eq__(a, b):
        if type(a) == type(b):
            if a.modifier == b.modifier:
                return True

        return False


class MovieClip(Writable):

    MOVIECLIP_END_FRAME_TAG = 0

    MOVIECLIP_FRAME_TAGS = (5, 11)
    MOVIECLIP_SCALING_GRID_TAG = 31
    MOVIECLIP_MATRIX_BANK_TAG = 41

    def __init__(self) -> None:
        super().__init__()

        self.frame_rate: int = 30
        self.binds: list[dict] = []
        self.frames: list[MovieClipFrame] = []

        self.nine_slice: list = []
        self.matrix_bank: int = 0

        self.unknown_flag: bool = False

    def load(self, swf, tag: int):
        id = swf.reader.read_ushort()

        self.frame_rate = swf.reader.read_uchar()
        frames_count = swf.reader.read_ushort()
        self.frames = [_class() for _class in [MovieClipFrame] * frames_count]

        self.unknown_flag = tag == 35

        if tag == 14:
            Console.error(
                "Tags MovieClip and MovieClip4 is unsupported! Aborting...")
            raise TypeError()
        
        if (tag == 49):
            custom_property = swf.reader.read_uchar()
            for _ in range(custom_property):
                property_type = swf.reader.read_uchar()
                match property_type:
                    case 0:
                        Console.warning(f"MovieClip {id} | Custom Property (Boolean): {swf.reader.read_uchar()}")
                    case _:
                        raise Exception(f"Unknown custom property {property_type} at {swf.reader.tell()}")

        if (tag != 3):
            frame_elements = []
            frame_elements_count = swf.reader.read_int()
            for x in range(frame_elements_count):
                bind_index = swf.reader.read_ushort()
                matrix_index = swf.reader.read_ushort()
                color_index = swf.reader.read_ushort()

                frame_elements.append({
                    "bind": bind_index,
                    "matrix": matrix_index,
                    "color": color_index
                })

        binds_count = swf.reader.read_ushort()

        for x in range(binds_count):
            self.binds.append({
                "id": swf.reader.read_ushort(),
                "blend": BLENDMODES[0]
            })

        if tag in (12, 35, 49):
            for x in range(binds_count):
                blend_index = swf.reader.read_uchar() & 0x3F
                # reversed = (bind_index >> 6) & 1 # TODO: blend modes
                self.binds[x]["blend"] = BLENDMODES[blend_index]

        for x in range(binds_count):
            self.binds[x]["name"] = swf.reader.read_ascii()

        frames_loaded = 0
        frame_elements_offset = 0
        while True:
            frame_tag = swf.reader.read_uchar()
            frame_tag_length = swf.reader.read_int()

            if frame_tag == MovieClip.MOVIECLIP_END_FRAME_TAG:
                break

            if frame_tag in MovieClip.MOVIECLIP_FRAME_TAGS:
                elements_count = self.frames[frames_loaded].load(swf)
                if frame_tag == 5:
                    for x in range(elements_count):
                        self.frames[frames_loaded].elements.append(
                            {
                                "bind": swf.reader.read_ushort(),
                                "matrix": swf.reader.read_ushort(),
                                "color": swf.reader.read_ushort()
                            }
                        )
                else:
                    for x in range(elements_count):
                        self.frames[frames_loaded].elements.append(
                            frame_elements[frame_elements_offset + x])
                    frame_elements_offset += elements_count
                    
                frames_loaded += 1
                continue

            elif frame_tag == MovieClip.MOVIECLIP_SCALING_GRID_TAG:
                self.nine_slice = [swf.reader.read_twip() for _ in range(4)]
                continue

            elif frame_tag == MovieClip.MOVIECLIP_MATRIX_BANK_TAG:
                self.matrix_bank = swf.reader.read_uchar()
                continue

            Console.warning(
                f"MovieClip {id} has unknown frame tag {frame_tag} with length {frame_tag_length} at {swf.reader.tell()}! Skipping...")
            swf.reader.skip(frame_tag_length)

        return id

    def save(self, id: int, ids: list):
        super().save()

        self.write_ushort(id)
        self.write_uchar(self.frame_rate)
        self.write_ushort(len(self.frames))

        frame_elements = []
        for frame in self.frames:
            for element in frame.elements:
                frame_elements.append(element)

        self.write_int(len(frame_elements))
        for element in frame_elements:
            self.write_ushort(element["bind"])
            self.write_ushort(element["matrix"])
            self.write_ushort(element["color"])

        self.write_ushort(len(self.binds))

        for bind in self.binds:
            self.write_ushort(ids[bind["id"]])

        for bind in self.binds:
            self.write_uchar(BLENDMODES.index(bind["blend"]) & 0x3F)

        for bind in self.binds:
            self.write_ascii(bind["name"])

        if self.matrix_bank > 0:
            self.write_uchar(41)
            self.write_int(1)
            self.write_uchar(self.matrix_bank)

        for frame in self.frames:
            tag_frame, buffer = frame.save()

            self.write_uchar(tag_frame)
            self.write_int(len(buffer))
            self.write(buffer)

        if self.nine_slice:
            self.write_uchar(31)
            self.write_int(16)

            x, y, width, height = self.nine_slice
            self.write_twip(x)
            self.write_twip(y)
            self.write_twip(width)
            self.write_twip(height)

        self.write(bytes(5))  # end tag for frame tags array

        # TODO: add support for tag 35 (idk where difference, but it's also used in games)
        return 12, self.buffer

    def __eq__(a, b):
        if type(a) == type(b):
            if a.frame_rate == b.frame_rate\
                    and a.binds == b.binds\
                    and a.frames == b.frames\
                    and a.nine_slice == b.nine_slice\
                    and a.matrix_bank == b.matrix_bank:
                return True

        return False


class MovieClipFrame(Writable):
    def __init__(self) -> None:
        self.elements: list = []
        self.name: str = None

    def load(self, swf):
        elements_count = swf.reader.read_ushort()
        self.name = swf.reader.read_ascii()

        return elements_count

    def save(self):
        super().save()

        self.write_ushort(len(self.elements))
        self.write_ascii(self.name)

        return 11, self.buffer

    def __eq__(a, b):
        if a.name == b.name\
                and a.elements == b.elements:
            return False
