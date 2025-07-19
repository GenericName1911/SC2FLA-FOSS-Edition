from zlib import decompress, compress

import numpy as np

from lib.utils import BinaryWriter
from lib.utils import BinaryReader

from PIL import Image


class Bitmap:
    @staticmethod
    def load(filepath: str):
        with open(filepath, 'rb') as file:
            content = file.read()

        stream = BinaryReader(content)

        magic = stream.read_short()

        if magic != 1283:
            raise Exception(f"Bad \".dat\" file: {filepath}")

        stream.skip(2)  # row data length

        width = stream.read_ushort()
        height = stream.read_ushort()

        stream.skip(4)  # unknown
        stream.skip(4)  # width in twips

        stream.skip(4)  # unknown
        stream.skip(4)  # height in twips

        flags = stream.read_uchar()
        compression = stream.read_bool()

        header = bytes()
        if compression:
            header_length = stream.read_ushort()
            header = stream.read(header_length)

        alpha = (flags & 1) != 0

        image_binary_data = bytes()
        while True:
            data_block_size = stream.read_ushort()

            if data_block_size == 0:
                break

            image_binary_data += stream.read(data_block_size)

        mode = 4 if alpha else 3

        if compression:
            image_binary_data = decompress(header + image_binary_data)

        array = np.frombuffer(image_binary_data, np.uint8)
        img = Image.fromarray(np.uint8(array))
        return img

    @staticmethod
    def save(filepath: str, image: Image, compression: bool = True):
        if image.mode == "LA":
            image = image.convert("RGBA")
        
        if image.mode == "L":
            image = image.convert("RGB")
        
        width, height = image.size
        alpha = image.mode == "RGBA"

        loaded = image.load()
        image_binary_data = []

        for y in range(height):
            for x in range(width):
                pixel = loaded[x, y]

                if alpha:
                    r, g, b, a = pixel
                    image_binary_data.append(b << 24 | g << 16 | r << 8 | a)
                else:
                    r, g, b = pixel
                    image_binary_data.append(b << 24 | g << 16 | r << 8)

        image_binary_data = np.array(image_binary_data, dtype="<I").tobytes()

        if compression:
            image_binary_data = compress(image_binary_data)

        stream = BinaryWriter()

        stream.write_ushort((height + width) * 2)
        stream.write_ushort(width)
        stream.write_ushort(height)
        stream.write_int(0)
        stream.write_int(width * 20)
        stream.write_int(0)
        stream.write_int(height * 20)
        stream.write_uchar(alpha)
        stream.write_bool(compression)

        if compression:
            header = image_binary_data[:2]

            stream.write_ushort(len(header))
            stream.write(header)

            image_binary_data = image_binary_data[2:]

        if len(image_binary_data) < 2048:
            stream.write_ushort(len(image_binary_data))
            stream.write(image_binary_data)

        else:
            blocks = [image_binary_data[i:i + 2048] for i in range(0, len(image_binary_data), 2048)]
            for block in blocks:
                stream.write_ushort(len(block))
                stream.write(block)

        with open(filepath, 'wb') as file:
            file.write(b"\x03\x05" + stream.buffer + b"\x00\x00")
