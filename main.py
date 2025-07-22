import os
import sys
import time
import struct
import shutil
import argparse
import subprocess
import logging

from sc_compression.signatures import Signatures
from sc_compression import Decompressor, Compressor
from lib.console import Console, Time

EXE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "lib", "ScDowngrade.exe"))

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[35m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[31m',
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        return f"{color}[{record.levelname}] {record.getMessage()}{self.RESET}"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter())
logger.handlers = [handler]

def sc_file_filter(path):
    return path.endswith(".sc") and not path.endswith("_tex.sc")

def print_centered(text, color_code=""):
    width = shutil.get_terminal_size().columns
    print(f"{color_code}{text.center(width)}\033[0m")

def get_used_version(data):
    if len(data) < 6 or data[:2] != b"SC":
        return None
    be = struct.unpack(">I", data[2:6])[0]
    le = struct.unpack("<I", data[2:6])[0]
    return le if be >= 5 else be

def downgrade(filepath):
    try:
        subprocess.run([EXE_PATH, filepath, filepath], check=True)
        logger.info(f"Downgraded: {os.path.basename(filepath)}")
    except FileNotFoundError:
        logger.error(f"Missing ScDowngrade.exe at path: {EXE_PATH}")
    except subprocess.CalledProcessError:
        logger.error(f"ScDowngrade.exe failed on: {os.path.basename(filepath)}")
    except Exception as e:
        logger.error(f"Unexpected error: {os.path.basename(filepath)} — {e}")

def decompile(filepath):
    from lib import sc_to_fla
    sc_to_fla(filepath)

def process_file(filepath):
    from lib import sc_to_fla

    logger.info(f"Processing: {os.path.basename(filepath)}")

    if not filepath.lower().endswith(".sc"):
        logger.warning(f"Invalid file extension: {os.path.basename(filepath)}")
        return

    with open(filepath, "rb") as f:
        data = f.read()

    version = get_used_version(data)
    if version is None:
        logger.critical(f"Bad File Magic: {os.path.basename(filepath)}")
        return

    if version >= 5:
        logger.info("SC2 file detected, downgrading")
        if not os.path.isfile(EXE_PATH):
            logger.critical(f"ScDowngrade.exe missing at {EXE_PATH}")
            exit()
        downgrade(filepath)
        with open(filepath, "rb") as f:
            data = f.read()
        version = get_used_version(data)
        if version is None or version >= 5:
            logger.error(f"Downgrade failed or version check invalid: {os.path.basename(filepath)}")
            return

    logger.info("Decompiling SC1 file")
    sc_to_fla(filepath)

def main():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="SC2FLA Toolkit — github.com/scwmake/SC | FOSS Support - github.com/GenericName1911",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=35, width=100),
        add_help=False
    )
    parser.add_argument("-p", "--process", type=str, metavar='FILE/DIR', help="Process .sc file or directory")
    parser.add_argument("-dx", "--decompress", type=str, metavar='FILE', help="Decompress .sc files")
    parser.add_argument("-cx", "--compress", type=str, metavar='FILE', help="Compress .sc files (LZMA | SC | v1)")
    parser.add_argument("-s", "--sort-layers", action="store_true", help="Enable layer sorting during decompilation")
    parser.add_argument("-d", "--dump", action="store_true", help="Dumps .png resources of .sc files (not implemented)")
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")

    args = parser.parse_args()
    start_time = time.time()

    if args.help or len(sys.argv) == 1:
        print()
        print_centered("FOSS Support by GenericName1911 - github.com/GenericName1911", "\033[95m")
        print_centered("SC2FLA Toolkit by SCW Make - github.com/scwmake/SC", "\033[32m")
        print("\nusage: main.py [-h] [-p] [-d] [-dx/-cx] [-s] input")
        print("\nArguments:")
        print("  -h,  --help             Show this help message and exit")
        print("  -p,  --process          Process .sc file or directory")
        print("  -d,  --dump             Dumps .png resources of .sc files (NOT IMPLEMENTED)")
        print("  -dx, --decompress       Decompress .sc files")
        print("  -cx, --compress         Compress .sc files (LZMA | SC | V1)")
        print("  -s,  --sort-layers      Enable layer sorting")
        

        print(f"\nDone in {Time(time.time() - start_time)} seconds.")
        return

    if args.process:
        path = os.path.abspath(args.process)
        if os.path.isfile(path) and sc_file_filter(path):
            process_file(path)
        elif os.path.isdir(path):
            for name in os.listdir(path):
                full = os.path.join(path, name)
                if os.path.isfile(full) and sc_file_filter(full):
                    process_file(full)
        else:
            logger.critical(f"Invalid input: {path}")
            exit()

    elif args.decompress:
        file = args.decompress
        if os.path.isfile(file):
            with open(file, 'rb') as f:
                raw = f.read().split(b"START")[0]
            dec = Decompressor().decompress(raw)
            with open(file + ".dec", 'wb') as out:
                out.write(dec)

    elif args.compress:
        file = args.compress
        if os.path.isfile(file):
            with open(file, 'rb') as f:
                raw = f.read()
            cmp = Compressor().compress(raw, Signatures.SC, 1)
            with open(file + ".cmp", 'wb') as out:
                out.write(cmp)

    elif args.dump:
        logger.warning("Dump feature has not been implemented yet!")

    print(f"Done in {Time(time.time() - start_time)} seconds.")

if __name__ == "__main__":
    main()
