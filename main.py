import os
import time
import argparse
import shutil

from sc-compression.signatures import Signatures
from sc-compression import Decompressor, Compressor

from lib.console import Console, Time


def sc_file_filter(path):
    return path.endswith(".sc") and not path.endswith("_tex.sc")


def print_centered(text, color_code=""):
    width = shutil.get_terminal_size().columns
    padded = text.center(width)
    print(f"{color_code}{padded}\033[0m")


def main():
    parser = argparse.ArgumentParser(description="SC tool by SCW Make - github.com/scwmake/SC")
    parser.add_argument("-d", "--decompile", help="Convert *.sc file to *.fla", type=str)
    parser.add_argument("-dx", "--decompress", help="Decompress *.sc files with Supercell compression", type=str)
    parser.add_argument("-cx", "--compress", help="Compress *.sc files with Supercell compression (LZMA | SC | version 1)", type=str)
    parser.add_argument("-s", "--sort-layers", help="Enable/disable layer sorting when decompiling", action="store_true")

    args = parser.parse_args()
    start_time = time.time()

    if args.decompile:
        from lib import sc_to_fla
        path = args.decompile

        if os.path.isdir(path):
            for file in os.listdir(path):
                filepath = os.path.join(path, file)
                if sc_file_filter(filepath):
                    target = filepath.replace(".sc", ".fla")
                    if not os.path.exists(target):
                        sc_to_fla(filepath)
        elif os.path.isfile(path) and sc_file_filter(path):
            sc_to_fla(path)

    elif args.decompress:
        file = args.decompress
        if os.path.isfile(file):
            with open(file, 'rb') as f:
                raw = f.read().split(b"START")[0]
            decompressed = Decompressor().decompress(raw)
            with open(file + ".dec", 'wb') as out:
                out.write(decompressed)

    elif args.compress:
        file = args.compress
        if os.path.isfile(file):
            with open(file, 'rb') as f:
                raw = f.read()
            compressed = Compressor().compress(raw, Signatures.SC, 1)
            with open(file + ".cmp", 'wb') as out:
                out.write(compressed)

    else:
        print()
        print_centered("FOSS Support by GenericName1911 - github.com/GenericName1911", "\033[95m")
        print_centered("SC2FLA Toolkit by SCW Make - github.com/scwmake/SC", "\033[32m")

        print("\nArguments:")
        print("  -d,   --decompile       Convert .sc (Supercell file) to .fla (Flash file)")
        print("  -dx,  --decompress      Decompress .sc files using Supercell compression")
        print("  -cx,  --compress        Compress .sc files using Supercell Compression (LZMA | SC | V1)")
        print("  -s,   --sort-layers     Enable layer sorting during decompilation (default: off)")

    print(f"Done in {Time(time.time() - start_time)} seconds.")

if __name__ == "__main__":
    main()
