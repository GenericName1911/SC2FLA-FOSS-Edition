import os

import time
import argparse

from sc_compression.signatures import Signatures
from sc_compression import Decompressor, Compressor

from lib.console import Console, Time

def main():
    parser = argparse.ArgumentParser(description="SC tool by SCW Make - github.com/scwmake/SC")

    parser.add_argument("-d", "--decompile", help="Convert *.sc file to *.fla", type=str)
    parser.add_argument("-dx", "--decompress", help="Decompress *.sc files with Supercell compression", type=str)
    parser.add_argument("-cx", "--compress", help="Compress *.sc files with Supercell compression (LZMA | SC | version 1)", type=str)
    parser.add_argument("-s", "--sort-layers", help="Convert *.sc file to *.fla", type=bool, default=True)

    args = parser.parse_args()

    start_time = time.time()

    if args.decompile:
        from lib import sc_to_fla
        path = args.decompile
        if os.path.isdir(path):
            for file in os.listdir(path):
                filepath = os.path.join(path, file)
                if filepath.endswith(".sc") and not filepath.endswith("_tex.sc"):
                    if os.path.exists(filepath.replace(".sc", ".fla")):
                        continue
                    else:
                        sc_to_fla(filepath)

        else:
            sc_to_fla(path)

    elif args.decompress:
        file = args.decompress

        decompressor = Decompressor()
        decompressed = decompressor.decompress(open(file, 'rb').read().split(b"START")[0])

        open(file + ".dec", 'wb').write(decompressed)

    elif args.compress:
        file = args.compress

        compressor = Compressor()
        compressed = compressor.compress(open(file, 'rb').read(), Signatures.SC, 1)

        open(file + ".cmp", 'wb').write(compressed)


    else:
        Console.title("SC tool by SCW Make - github.com/scwmake/SC")
        print("-d, --decompile : Convert *.sc file to *.fla")
        print("-dx, --decompress : Decompress *.sc files with Supercell compression")
        print("-cx, --compress : Compress *.sc files with Supercell compression (LZMA | SC | version 1)")
        exit(0)

    result_time = time.time() - start_time

    print(f"Done in {Time(result_time)} seconds!")


if __name__ == "__main__":
    main()
