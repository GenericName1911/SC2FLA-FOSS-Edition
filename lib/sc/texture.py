from .writable import Writable
import tempfile
import os
from PIL import Image
import colorama
import zstandard
import io
import subprocess
from lib.utils.reader import BinaryReader
from lib.utils.writer import BinaryWriter
from lib.sc.streaming.sctx import SCTX
from lib.sc.streaming.scPixel import ScPixel
from lib.console import Console

colorama.init()

PACKER_FILTER_TABLE = {
    "LINEAR": "GL_LINEAR",
    "NEAREST": "GL_NEAREST",
    "MIPMAP": "GL_LINEAR_MIPMAP_NEAREST"
}

PACKER_PIXEL_TYPES = [
    "RGBA8888", "BGRA8888", "RGBA4444", "RGBA5551", "RGB565",
    "RGBA8888", "ALPHA_INTENSITY", "RGBA8888", "RGBA8888", "ALPHA"
]

MODES_TABLE = {
    "GL_RGBA": "RGBA",
    "GL_RGB": "RGB",
    "GL_LUMINANCE_ALPHA": "LA",
    "GL_LUMINANCE": "L"
}

CHANNLES_TABLE = {
    "RGBA": 4,
    "RGB": 3,
    "LA": 2,
    "L": 1
}

PIXEL_TYPES = [
    "GL_UNSIGNED_BYTE", "GL_UNSIGNED_BYTE", "GL_UNSIGNED_SHORT_4_4_4_4",
    "GL_UNSIGNED_SHORT_5_5_5_1", "GL_UNSIGNED_SHORT_5_6_5",
    "GL_UNSIGNED_BYTE", "GL_UNSIGNED_BYTE", "GL_UNSIGNED_BYTE",
    "GL_UNSIGNED_BYTE", "GL_UNSIGNED_SHORT_4_4_4_4", "GL_UNSIGNED_BYTE"
]

PIXEL_FORMATS = [
    "GL_RGBA", "GL_RGBA", "GL_RGBA", "GL_RGBA", "GL_RGB", "GL_RGBA",
    "GL_LUMINANCE_ALPHA", "GL_RGBA", "GL_RGBA", "GL_RGBA", "GL_LUMINANCE"
]

PIXEL_INTERNAL_FORMATS = [
    "GL_RGBA8", "GL_RGBA8", "GL_RGBA4", "GL_RGB5_A1", "GL_RGB565",
    "GL_RGBA8", "GL_LUMINANCE8_ALPHA8", "GL_RGBA8", "GL_RGBA8",
    "GL_RGBA4", "GL_LUMINANCE8"
]

def read_rgba8(swf): return tuple(swf.reader.read_uchar() for _ in range(4))

def read_rgba4(swf):
    p = swf.reader.read_ushort()
    return ((p >> 12) & 15) << 4, ((p >> 8) & 15) << 4, ((p >> 4) & 15) << 4, (p & 15) << 4

def read_rgb5_a1(swf):
    p = swf.reader.read_ushort()
    return ((p >> 11) & 31) << 3, ((p >> 6) & 31) << 3, ((p >> 1) & 31) << 3, (p & 255) << 7

def read_rgb565(swf):
    p = swf.reader.read_ushort()
    return ((p >> 11) & 31) << 3, ((p >> 5) & 63) << 2, (p & 31) << 3

def read_luminance8_alpha8(swf):
    return swf.reader.read_uchar(), swf.reader.read_uchar()

def read_luminance8(swf):
    return swf.reader.read_uchar()

def write_rgba8(swf, p): [swf.write_uchar(c) for c in p]

def write_rgba4(swf, p): swf.write_ushort(p[3] >> 4 | p[2] >> 4 << 4 | p[1] >> 4 << 8 | p[0] >> 4 << 12)

def write_rgb5_a1(swf, p): swf.write_ushort(p[3] >> 7 | p[2] >> 3 << 1 | p[1] >> 3 << 6 | p[0] >> 3 << 11)

def write_rgb565(swf, p): swf.write_ushort(int(p[2] >> 3 | p[1] >> 2 << 5 | p[0] >> 3 << 11))

def write_luminance8_alpha8(swf, p): swf.write_ushort(p[0] << 8 | p[1])

def write_luminance8(swf, p): swf.write_uchar(int(p))

PIXEL_READ_FUNCTIONS = {
    "GL_RGBA8": read_rgba8,
    "GL_RGBA4": read_rgba4,
    "GL_RGB5_A1": read_rgb5_a1,
    "GL_RGB565": read_rgb565,
    "GL_LUMINANCE8_ALPHA8": read_luminance8_alpha8,
    "GL_LUMINANCE8": read_luminance8
}

PIXEL_WRITE_FUNCTIONS = {
    "GL_RGBA8": write_rgba8,
    "GL_RGBA4": write_rgba4,
    "GL_RGB5_A1": write_rgb5_a1,
    "GL_RGB565": write_rgb565,
    "GL_LUMINANCE8_ALPHA8": write_luminance8_alpha8,
    "GL_LUMINANCE8": write_luminance8
}

def get_aligned_bytes_position(pos): return pos if pos % 16 == 0 else (pos // 16 + 1) * 16

class SWFTexture(Writable):
    def __init__(self):
        self.channels = 4
        self.pixel_format = "GL_RGBA"
        self.pixel_internal_format = "GL_RGBA8"
        self.pixel_type = "GL_UNSIGNED_BYTE"
        self.mag_filter = "GL_LINEAR"
        self.min_filter = "GL_NEAREST"
        self.linear = True
        self.downscaling = True
        self.width = 0
        self.height = 0
        self._image = None

    def load_khronos_texture(self, data):
        inputPath = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()) + ".ktx")
        outputPath = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()) + ".png")
        with open(inputPath, "wb") as f: f.write(data)
        os.system(f"PVRTexToolCLI.exe -i {inputPath} -d {outputPath} -ics sRGB -noout")
        self._image = Image.open(outputPath)

    def load(self, swf, tag, has_external_texture):
        ktxSize = 0
        externalTextureFilepath = ""
        if tag == 45: ktxSize = swf.reader.read_uint()
        if tag == 47: externalTextureFilepath = swf.reader.read_ascii()

        pixel_type_index = swf.reader.read_uchar()
        self.pixel_format = PIXEL_FORMATS[pixel_type_index]
        self.pixel_internal_format = PIXEL_INTERNAL_FORMATS[pixel_type_index]
        self.pixel_type = PIXEL_TYPES[pixel_type_index]

        self.mag_filter, self.min_filter = "GL_LINEAR", "GL_NEAREST"
        if tag in [16, 19, 29]: self.min_filter = "GL_LINEAR_MIPMAP_NEAREST"
        elif tag == 34: self.mag_filter = self.min_filter = "GL_NEAREST"

        self.linear = tag not in [27, 28, 29]
        self.downscaling = tag in [1, 16, 28, 29]

        self.width = swf.reader.read_ushort()
        self.height = swf.reader.read_ushort()

        if ktxSize:
            self.load_khronos_texture(swf.reader.read(ktxSize))
            return

        if externalTextureFilepath:
            ext = externalTextureFilepath.split(".")[-1]
            path = os.path.join(os.path.dirname(swf.filename), externalTextureFilepath)

            if ext == "zktx":
                dctx = zstandard.ZstdDecompressor()
                buf = io.BytesIO()
                with open(path, "rb") as f: dctx.copy_stream(f, buf)
                self.load_khronos_texture(buf.getvalue())

            elif ext == "ktx":
                self.load_khronos_texture(open(path, "rb").read())

            elif ext == "sctx":
                    print(colorama.Fore.LIGHTMAGENTA_EX + "[INFO] Extracting External Asset Texture:", externalTextureFilepath)
                    out = path.replace("sctx", "png")
                    conv = os.path.relpath(os.path.join(os.path.dirname(__file__), "..", "SctxConverter.exe"))
                    try:
                        subprocess.run([conv, "decode", path, out, "-t"], check=True)
                        print(colorama.Fore.LIGHTMAGENTA_EX + "[INFO] SCTX decoded to:", os.path.basename(out))
                        self._image = Image.open(out)

                        ktx_writer = BinaryWriter()
                        streaming = SCTX(path, swf.streaming_lowres_id)
                        ktx_writer.write(b'\xabKTX 11\xbb\r\n\x1a\n')
                        ktx_writer.write(b'\x01\x02\x03\x04')
                        ktx_writer.write_uint(0)
                        ktx_writer.write_uint(1)
                        ktx_writer.write_uint(0)
                        ktx_writer.write_uint(ScPixel.glInternalFormat(streaming.texture.pixel_type))
                        ktx_writer.write_uint(6408)
                        ktx_writer.write_uint(streaming.texture.width)
                        ktx_writer.write_uint(streaming.texture.height)
                        ktx_writer.write_uint(0)
                        ktx_writer.write_uint(0)
                        ktx_writer.write_uint(1)
                        ktx_writer.write_uint(1)
                        ktx_writer.write_uint(0)
                        ktx_writer.write_uint(streaming.texture.data_length)
                        ktx_writer.write(streaming.texture.data)
                        self.load_khronos_texture(ktx_writer.buffer)

                    except FileNotFoundError:
                        print(colorama.Fore.RED + "[CRITICAL] Missing SctxConverter.exe")
                        return
                    except subprocess.CalledProcessError:
                        print(colorama.Fore.RED + "[ERROR] SctxConverter.exe failed")
                        return  
                    except Exception as e:
                        print(colorama.Fore.RED + "[ERROR] Unexpected error:", e)
                        return
            return

        if not has_external_texture:
            Console.info(f"SWFTexture: {self.width}x{self.height} - Format: {self.pixel_type} {self.pixel_format} {self.pixel_internal_format}")
            self._image = Image.new(MODES_TABLE[self.pixel_format], (self.width, self.height))
            loaded = self._image.load()
            self.channels = CHANNLES_TABLE[self._image.mode]
            read_pixel = PIXEL_READ_FUNCTIONS[self.pixel_internal_format]

            if self.linear:
                for y in range(self.height):
                    for x in range(self.width): loaded[x, y] = read_pixel(swf)
                    Console.progress_bar("Loading texture data...", y, self.height)
                print()
            else:
                block = 32
                for yb in range((self.height // block) + 1):
                    for xb in range((self.width // block) + 1):
                        for y in range(block):
                            py = yb * block + y
                            if py >= self.height: break
                            for x in range(block):
                                px = xb * block + x
                                if px >= self.width: break
                                loaded[px, py] = read_pixel(swf)
                    Console.progress_bar("Loading splitted texture data...", yb, (self.height // block) + 1)
                print()

    def save(self, has_external_texture):
        super().save()
        pixel_type_index = PIXEL_INTERNAL_FORMATS.index(self.pixel_internal_format)
        tag = 1

        if (self.mag_filter, self.min_filter) == ("GL_LINEAR", "GL_NEAREST"):
            tag = 24 if self.linear else (28 if self.downscaling else 27)
        elif (self.mag_filter, self.min_filter) == ("GL_LINEAR", "GL_LINEAR_MIPMAP_NEAREST"):
            tag = 19 if self.downscaling else (29 if not self.linear else 16)
        elif (self.mag_filter, self.min_filter) == ("GL_NEAREST", "GL_NEAREST"):
            tag = 34

        self.write_uchar(pixel_type_index)
        self.write_ushort(self.width)
        self.write_ushort(self.height)
        Console.info(f"SWFTexture: {self.width}x{self.height} - Format: {self.pixel_type} {self.pixel_format} {self.pixel_internal_format}")

        if not has_external_texture:
            loaded = self._image.load()
            write_pixel = PIXEL_WRITE_FUNCTIONS[self.pixel_internal_format]
            if not self.linear:
                clone = self._image.copy().load()
                idx = 0
                for yb in range((self.height // 32) + 1):
                    for xb in range((self.width // 32) + 1):
                        for y in range(32):
                            py = yb * 32 + y
                            if py >= self.height: break
                            for x in range(32):
                                px = xb * 32 + x
                                if px >= self.width: break
                                clone[idx % self.width, idx // self.width] = loaded[px, py]
                                idx += 1
                loaded = clone
            for y in range(self.height):
                Console.progress_bar("Writing texture data...", y, self.height)
                for x in range(self.width): write_pixel(self, loaded[x, y])
            print()

        return tag, self.buffer

    def get_image(self): return self._image

    def set_image(self, img):
        self._image = img
        self.channels = CHANNLES_TABLE[self._image.mode]
        self.width, self.height = self._image.size
        if self.channels == 4:
            self.pixel_format = "GL_RGBA"
            if self.pixel_type == "GL_UNSIGNED_BYTE":
                self.pixel_internal_format = "GL_RGBA8"
            elif self.pixel_type == "GL_UNSIGNED_SHORT_4_4_4_4":
                self.pixel_internal_format = "GL_RGBA4"
            else:
                self.pixel_internal_format = "GL_RGB5_A1"
        elif self.channels == 3:
            self.pixel_format = "GL_RGB"
            self.pixel_type = "GL_UNSIGNED_SHORT_5_6_5"
            self.pixel_internal_format = "GL_RGB565"
        elif self.channels == 2:
            self.pixel_format = "GL_LUMINANCE_ALPHA"
            self.pixel_type = "GL_UNSIGNED_BYTE"
            self.pixel_internal_format = "GL_LUMINANCE8_ALPHA8"
        else:
            self.pixel_format = "GL_LUMINANCE"
            self.pixel_type = "GL_UNSIGNED_BYTE"
            self.pixel_internal_format = "GL_LUMINANCE8"
