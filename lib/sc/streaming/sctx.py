from lib.utils.reader import BinaryReader
from lib.sc.streaming.scPixel import ScPixel
import zstandard
import io

class Texture:
    def __init__(self, pixel: ScPixel, width: int = 0, height: int = 0) -> None:
        self.width = width
        self.height = height
        self.data_length: int = 0
        self.data: bytes = None
        self.pixel_type: ScPixel = pixel
        


class SCTX:
    def __init__(self, filepath: str, streaming_id_override: int = 0xFF) -> None:
        self.width = 0
        self.height = 0
        
        # For now support only streaming texture id
        self.streaming_texture_id = streaming_id_override 
        self.texture_id = 0xFF
        # Since in SWF we have a tag with 2 ints (one for the streaming texture and the other for regular one i think), 
        # I have a guess that we can set these priorities from there, and if such a priority is equal to 0 for some of the textures, then it will not be read, 
        # so if you set the priority to 0 for the streaming texture,
        # then default streaming will be disabled because texture for streaming will be missing,
        # and regular texture will be loaded into memory immediately
        
        self.streaming_texture: Texture = None
        self.texture: Texture = None
        
        reader = BinaryReader(open(filepath, "rb").read())
        streaming_length = reader.read_uint()
        streaming_data = reader.read(streaming_length)
        
        self.read_streaming_data(streaming_data)
        
        data_length = reader.read_uint()
        data = reader.read(data_length)
        
        self.read_texture(data)
        self.texture.data = reader.read(self.texture.data_length)
    
    def read_streaming_data(self, data: bytes):
        reader = BinaryReader(data)
        
        header_length = reader.read_uint()
        
        # Very strange buffer with file magic. Skip for now.
        reader.skip(header_length)
        
        # Texture Info
        pixel_type = reader.read_uint()
        width = reader.read_ushort()
        height = reader.read_ushort()
        reader.read_int()

        self.texture = Texture(ScPixel(pixel_type), width, height)
        self.texture.data_length = reader.read_uint()
                
        if (self.streaming_texture_id != 0):
            reader.skip(16)
            
            streaming_texture_length = reader.read_uint()
            self.read_streaming_texture(reader.read(streaming_texture_length))
            self.streaming_id = reader.read_uint()
        
    def read_streaming_texture(self, data: bytes):
        reader = BinaryReader(data)
        
        # 28 bytes of bullshit
        reader.skip(28)
        
        width = reader.read_ushort()
        height = reader.read_ushort()
        pixel_type = reader.read_uint()
        reader.read_int()
        
        self.streaming_texture = Texture(ScPixel(pixel_type), width, height)
        self.streaming_texture.data_length = reader.read_uint()
        self.streaming_texture.data = reader.read(self.streaming_texture.data_length)
        
    def read_texture(self, data: bytes):
        reader = BinaryReader(data)
        
        reader.skip(24)
        
        self.texture.width = reader.read_ushort()
        self.texture.height = reader.read_ushort()
        reader.read_uint()
        
        # Idk for sure but yeah
        hash_length = reader.read_uint()
        hash = reader.read(hash_length)