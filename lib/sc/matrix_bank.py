from .writable import Writable
import numpy

class Color:
    def __init__(self,
                 r_add: float = 0.0,
                 g_add: float = 0.0,
                 b_add: float = 0.0,
                 a_mul: float = 1.0,
                 r_mul: float = 1.0,
                 g_mul: float = 1.0,
                 b_mul: float = 1.0) -> None:

        self.r_add = r_add
        self.g_add = g_add
        self.b_add = b_add

        self.a_mul = a_mul
        self.r_mul = r_mul
        self.g_mul = g_mul
        self.b_mul = b_mul

    def load(self, swf, tag):
        self.r_add = swf.reader.read_uchar()
        self.g_add = swf.reader.read_uchar()
        self.b_add = swf.reader.read_uchar()

        self.a_mul = swf.reader.read_uchar() / 255
        self.r_mul = swf.reader.read_uchar() / 255
        self.g_mul = swf.reader.read_uchar() / 255
        self.b_mul = swf.reader.read_uchar() / 255

    def save(self, swf):
        swf.writer.write_uchar(9)
        swf.writer.write_int(7)

        swf.writer.write_uchar(round(self.r_add))
        swf.writer.write_uchar(round(self.g_add))
        swf.writer.write_uchar(round(self.b_add))

        swf.writer.write_uchar(round(self.a_mul * 255))
        swf.writer.write_uchar(round(self.r_mul * 255))
        swf.writer.write_uchar(round(self.g_mul * 255))
        swf.writer.write_uchar(round(self.b_mul * 255))

class Matrix:
    def __init__(self,
                 a: int = 1,
                 b: int = 0,
                 c: int = 0,
                 d: int = 1,
                 tx: int = 0,
                 ty: int = 0) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.tx = tx
        self.ty = ty

    def load(self, swf, tag):
        divider = 1024 if tag == 8 else 65535

        self.a = swf.reader.read_int() / divider  # scale x
        self.b = swf.reader.read_int() / divider  # rotation x
        self.c = swf.reader.read_int() / divider  # rotation y
        self.d = swf.reader.read_int() / divider  # scale y

        self.tx = swf.reader.read_twip()  # position x
        self.ty = swf.reader.read_twip()  # position y

    def save(self, swf):
        swf.writer.write_uchar(8)
        swf.writer.write_int(24)

        swf.writer.write_int(int(round(self.a * 1024)))
        swf.writer.write_int(int(round(self.b * 1024)))
        swf.writer.write_int(int(round(self.c * 1024)))
        swf.writer.write_int(int(round(self.d * 1024)))

        swf.writer.write_twip(self.tx)
        swf.writer.write_twip(self.ty)

    def __eq__(a, b):
        if type(a) == type(b):
            if a.a == b.a and a.b == b.b and a.c == b.c and a.d == b.d and a.tx == b.tx and a.ty == b.ty:
                return True

        return False


class MatrixBank(Writable):
    def __init__(self) -> None:
        self.index: int = 0

        self.matrices: list = []
        self.color_transforms: list = []

        self.matrices_count: int = 0
        self.color_transforms_count: int = 0

    def available_for_matrix(self, count=0):
        if len(self.matrices) >= 65534 - count:
            return False
        return True

    def available_for_colors(self, count=0):
        if len(self.color_transforms) >= 65534 - count:
            return False
        return True

    def get_matrix(self, matrix: Matrix):
        if isinstance(matrix, list):
            matrix = Matrix(matrix[0],
                            matrix[1],
                            matrix[2],
                            matrix[3],
                            matrix[4],
                            matrix[5])
        elif isinstance(matrix, dict):
            matrix = Matrix(matrix["a"],
                            matrix["b"],
                            matrix["c"],
                            matrix["d"],
                            matrix["tx"],
                            matrix["ty"])

        if matrix not in self.matrices:
            self.matrices.append(matrix)

        return self.matrices.index(matrix)

    def get_color_transform(self, color_transform: list):
        if color_transform not in self.color_transforms:
            self.color_transforms.append(color_transform)

        return self.color_transforms.index(color_transform)

    def load(self, swf):
        self.matrices_count = swf.reader.read_ushort()
        self.color_transforms_count = swf.reader.read_ushort()

        self.matrices = [_class() for _class in [Matrix] * self.matrices_count]
        self.color_transforms= [_class() for _class in [Color] * self.color_transforms_count]

    def save(self):
        super().save()

        self.write_ushort(len(self.matrices))
        self.write_ushort(len(self.color_transforms))

        return 42, self.buffer
