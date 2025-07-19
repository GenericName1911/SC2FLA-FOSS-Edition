from io import BytesIO


class BinaryWriter(BytesIO):
    def __init__(self, initial_bytes: bytes = b"") -> None:
        super().__init__(initial_bytes)
    
    @property
    def buffer(self):
        return self.getvalue()
    
    def fill(self, size: int):
        self.write(b"\x00" * size)
    
    def write_bool(self, data: bool):
        self.write(int(data).to_bytes(1, "little"))
    
    def write_char(self, data: int):
        self.write(data.to_bytes(1, "little", signed=True))
    
    def write_uchar(self, data: int):
        self.write(data.to_bytes(1, "little", signed=False))
    
    def write_short(self, data: int):
        self.write(data.to_bytes(2, "little", signed=True))
    
    def write_ushort(self, data: int):
        self.write(data.to_bytes(2, "little", signed=False))
    
    def write_int(self, data: int):
        self.write(data.to_bytes(4, "little", signed=True))
        
    def write_uint(self, data: int):
        self.write(data.to_bytes(4, "little", signed=False))
    
    def write_ascii(self, data: str = None):
        if not data:
            self.write_uchar(0xFF)
        else:
            self.write_uchar(len(data))
            self.write(data.encode('ascii'))
    
    def write_twip(self, data: float):
        self.write_int(int(round(data * 20)))
