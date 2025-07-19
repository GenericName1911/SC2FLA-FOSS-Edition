from io import BytesIO


class BinaryReader(BytesIO):
    def __init__(self, initial_bytes: bytes) -> None:
        super().__init__(initial_bytes)

    def skip(self, size: int):
        self.read(size)

    def read_bool(self):
        return self.read_uchar() >= 1

    def read_char(self):
        return int.from_bytes(self.read(1), "little", signed=True)

    def read_uchar(self):
        return int.from_bytes(self.read(1), "little", signed=False)

    def read_short(self):
        return int.from_bytes(self.read(2), "little", signed=True)

    def read_ushort(self):
        return int.from_bytes(self.read(2), "little", signed=False)

    def read_int(self):
        return int.from_bytes(self.read(4), "little", signed=True)
    
    def read_uint(self):
        return int.from_bytes(self.read(4), "little", signed=False)

    def read_ascii(self):
        size = self.read_uchar()
        if size != 0xFF:
            return self.read(size).decode('utf8')
        return None

    def read_twip(self):
        return self.read_int() / 20
