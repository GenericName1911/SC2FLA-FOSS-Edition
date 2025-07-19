import os

from shutil import rmtree

from zipfile import ZipFile, ZIP_DEFLATED
from zipfile import BadZipfile

from lib.fla.dom.document import DOMDocument
from lib.fla.dom.folder_item import DOMFolderItem
from lib.fla.dom.bitmap_item import DOMBitmapItem
from lib.fla.dom.symbol_item import DOMSymbolItem
from lib.fla.dom.timeline import DOMTimeline
from lib.fla.dom.layer import DOMLayer
from lib.fla.dom.frame import DOMFrame
from lib.fla.dom.group import DOMGroup
from lib.fla.dom.bitmap_instance import DOMBitmapInstance
from lib.fla.dom.symbol_instance import DOMSymbolInstance
from lib.fla.dom.shape import DOMShape
from lib.fla.dom.static_text import DOMStaticText
from lib.fla.dom.dynamic_text import DOMDynamicText
from lib.fla.dom.text_run import DOMTextRun
from lib.fla.dom.text_attrs import DOMTextAttrs

from lib.fla.fill.fill_style import FillStyle
from lib.fla.fill.solid_color import SolidColor
from lib.fla.fill.gradient_entry import GradientEntry
from lib.fla.fill.linear_gradient import LinearGradient
from lib.fla.fill.radial_gradient import RadialGradient
from lib.fla.fill.bitmap_fill import BitmapFill

from lib.fla.stroke.stroke_style import StrokeStyle
from lib.fla.stroke.solid_stroke import SolidStroke

from lib.fla.edge.edge import Edge

from lib.fla.filter.glow_filter import GlowFilter
from lib.fla.filter.drop_shadow_filter import DrowShadowFilter

from lib.fla.geom.point import Point
from lib.fla.geom.matrix import Matrix
from lib.fla.geom.color_transform import ColorTransform
from lib.fla.geom.color import Color

from lib.fla.dat.bitmap import Bitmap

import io
import struct
# TODO move to custom zip/fla reader


class XFL:
    @staticmethod
    def load(projectpath: str):
        if os.path.isfile(projectpath):
            if os.path.splitext(projectpath)[1] != ".fla":
                raise Exception(f"File is not \".fla\": {projectpath}")

            fla_file = open(projectpath, "rb")
            folder = os.path.splitext(projectpath)[0]

            try:
                with ZipFile(fla_file, 'r') as file:
                    file.extractall(folder)

            except BadZipfile:
                EOCD_FORMAT = "<4s4H2LH"
                EOCD_SIZE = 22
                CDIR_SIZE_CORRECTION = 54

                real_seek = fla_file.seek
                real_read = fla_file.read

                def fake_seek(self, offset, whence=io.SEEK_SET):
                    if offset == -EOCD_SIZE and whence == io.SEEK_END:
                        # Perform the seek and get the zip's total size
                        zip_size = EOCD_SIZE + real_seek(offset, whence)
                        eocd_data = self.read()
                        eocd = list(struct.unpack(EOCD_FORMAT, eocd_data))
                        cdir_size = eocd[5]
                        cdir_offset = eocd[6]

                        # Assuming the central dir offset is right, is the size wrong?
                        actual_cdir_size = zip_size - cdir_offset - EOCD_SIZE
                        delta = cdir_size - actual_cdir_size
                        if delta == CDIR_SIZE_CORRECTION:
                            eocd[5] -= CDIR_SIZE_CORRECTION
                            eocd_data = struct.pack(EOCD_FORMAT, *eocd)
                        elif delta != 0:
                            raise Exception(
                                f"Central directory size is off by an unexpected amount: {delta}"
                            )

                        self.seek = real_seek

                        # Fake the next read() to return `eocd_data`
                        def fake_read(self, size=-1):
                            if size != -1:
                                # We expect read() to be called with no arguments
                                raise Exception(f"Expected size of -1, not {size}")
                            self.read = real_read
                            return eocd_data

                        self.read = fake_read.__get__(self)
                    else:
                        return real_seek(offset, whence)

                # __get__ turns a function into a method: https://stackoverflow.com/a/46757134
                fla_file.seek = fake_seek.__get__(fla_file)

                with ZipFile(fla_file, 'r') as file:
                    file.extractall(folder)

            return XFL.load(folder)

        elif os.path.isdir(projectpath):
            document = DOMDocument()
            document.load(projectpath)
            return document

        raise Exception(f"Project does not exist: {projectpath}")

    @staticmethod
    def save(document: DOMDocument):
        filepath = document.filepath + ".fla"

        projectpath = document.filepath

        if not os.path.exists(projectpath):
            os.mkdir(projectpath)

        document.save()

        with ZipFile(filepath, 'w', compression=ZIP_DEFLATED) as file:
            for root, _, files in os.walk(projectpath):
                for filename in files:
                    file.write(os.path.join(root, filename),
                               os.path.relpath(os.path.join(root, filename), os.path.join(projectpath, '')))

        rmtree(projectpath)
