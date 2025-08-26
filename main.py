import os
import sys
import time
import struct
import shutil
import argparse
import subprocess
import logging
import colorama
import importlib

from lib import sc_import
import sys as _sys
_sys.modules["sc_import"] = sc_import
_sys.modules["lib.sc_import"] = sc_import

from sc_compression.signatures import Signatures
from sc_compression import Decompressor, Compressor
from lib.console import Console, Time
from colorama import Fore, Style


sc1_ver = [1, 2, 3, 4]
sc2_ver = [5, 6]
EXE_PATH = os.path.relpath(os.path.join(os.path.dirname(__file__), "lib", "ScDowngrade.exe"))
colorama.init()

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.LIGHTMAGENTA_EX,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.LIGHTRED_EX,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, Style.RESET_ALL)
        return f"{color}[{record.levelname}] {record.getMessage()}{Style.RESET_ALL}"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter())
logger.handlers = [handler]


def verify_files():
    logger.info("Verifying File Integrity...")
    if not os.path.exists("lib/ScDowngrade.exe"):
        logger.warning("Missing ScDowngrade.exe")
    if not os.path.exists("lib/SctxConverter.exe"):
        logger.warning("Missing SctxConverter.exe")
   
def sc_file_filter(path):
    return path.endswith(".sc") and not path.endswith("_tex.sc")


def print_centered(text, color_code=""):
    width = shutil.get_terminal_size().columns
    print(f"{color_code}{text.center(width)}{Style.RESET_ALL}")


def get_used_version(data):
    if len(data) < 6 or data[:2] != b"SC":
        return None
    be = struct.unpack(">I", data[2:6])[0]
    le = struct.unpack("<I", data[2:6])[0]
    if be in sc1_ver or be in sc2_ver:
        return be
    if le in sc1_ver or le in sc2_ver:
        return le
    return None


def downgrade(filepath):
    try:
        subprocess.run([EXE_PATH, filepath, filepath], check=True)
        logger.info(f"Downgraded: {os.path.basename(filepath)}")
    except FileNotFoundError:
        logger.critical(f"Missing ScDowngrade.exe at path: ~\\{EXE_PATH}")
    except subprocess.CalledProcessError:
        logger.error(f"ScDowngrade.exe Failed on: {os.path.basename(filepath)}")
    except Exception as e:
        logger.error(f"Unexpected Error: {os.path.basename(filepath)} — {e}")


def process_file(filepath, dump):
    importlib.invalidate_caches()
    import lib.sc_import as sc_import
    importlib.reload(sc_import)
    sc_import.DUMP = dump
    from lib import sc_to_fla

    print("-" * 20)
    logger.info(f"Processing: {os.path.basename(filepath)}")

    with open(filepath, "rb") as f:
        data = f.read()

    version = get_used_version(data)
    if version is None:
        logger.critical(f"Bad File Magic: {os.path.basename(filepath)}")
        return

    if version in sc1_ver:
        sc_to_fla(filepath)
    elif version in sc2_ver:
        logger.info("SC2 file Detected - Downgrading")
        downgrade(filepath)

        with open(filepath, "rb") as f:
            data = f.read()
        version = get_used_version(data)

        if version is not None and version not in sc2_ver:
            logger.info("Processing SC1 file")
            sc_to_fla(filepath)
        else:
            logger.warning("Processing Failed! Skipping file...")
    else:
        logger.critical(f"Unsupported Version: {os.path.basename(filepath)}")


def dump_png():
    # placeholder
    pass


def main():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="SC2FLA Toolkit — github.com/scwmake/SC | FOSS Support - github.com/GenericName1911",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=35, width=100),
        add_help=False)
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
    parser.add_argument("-p", "--process", type=str, metavar='FILE/DIR', help="Process .sc file or directory")
    parser.add_argument("-dr", "--dump-raw", action="store_true", help="Dumps RAW resources of .sc files")
    parser.add_argument("-dp", "--dump-png", action="store_true", help="Dumps PNG resources of .sc files")
    parser.add_argument("-dx", "--decompress", type=str, metavar='FILE', help="Decompress .sc files")
    parser.add_argument("-cx", "--compress", type=str, metavar='FILE', help="Compress .sc files (LZMA | SC | v1)")
    parser.add_argument("-s", "--sort-layers", action="store_true", help="Enable layer sorting during decompilation")

    args = parser.parse_args()
    start_time = time.time()

    if args.help or len(sys.argv) == 1:
        print()
        print_centered("FOSS Support by GenericName1911 - github.com/GenericName1911", Fore.LIGHTMAGENTA_EX)
        print_centered("SC2FLA Toolkit by SCW Make - github.com/scwmake/SC", Fore.GREEN)
        print("\nusage: main.py [-h] [-p] [-d] [-dx/-cx] [-s] input")
        print("\nArguments:")
        print("  -h,  --help             Show this help message and exit")
        print("  -p,  --process          Process .sc file or directory")
        print("  -dr,  --dump-raw        Dumps RAW resources of .sc files")
        print("  -dp,  --dump-png        Dumps PNG resources of .sc files")
        print("  -dx, --decompress       Decompress .sc files")
        print("  -cx, --compress         Compress .sc files (LZMA | SC | V1)")
        print("  -s,  --sort-layers      Enable layer sorting")
        print(f"\nDone in {Time(time.time() - start_time)} seconds.")
        return
        
    verify_files()    
    
    if args.dump_raw:
        logger.info("Dump RAW Enabled.")
    else:
        logger.info("Dump RAW Disabled.")

    if args.dump_png:
        logger.info("Dump PNG Enabled.")
        dump_png()
    else:
        logger.info("Dump PNG Disabled.")
        
    if args.dump_raw and args.dump_png:
        logger.error("Both RAW and PNG dump cannot be enabled at the same time.")
        sys.exit(1)
    
    if args.sort_layers:
        logger.info("Layer Sorting Enabled.")
    else:
        logger.info("Layer Sorting Disabled.")
        
    if args.process:
        path = os.path.abspath(args.process)
        if os.path.isfile(path) and sc_file_filter(path):
            process_file(path, args.dump)
        elif os.path.isfile(path) and os.path.splitext(args.process)[1] != ".sc":
            logger.warning(f"Invalid File: {os.path.basename(args.process)}")
        elif os.path.isdir(path):
            for name in os.listdir(path):
                full = os.path.join(path, name)
                if os.path.isfile(full) and sc_file_filter(full):
                    process_file(full, args.dump)

    elif args.decompress:
        file = args.decompress
        logger.info(f"Decompressing: {os.path.basename(file)}")
        if os.path.isfile(file):
            with open(file, 'rb') as f:
                raw = f.read().split(b"START")[0]
            dec = Decompressor().decompress(raw)
            with open(file + ".dec", 'wb') as out:
                out.write(dec)

    elif args.compress:
        file = args.compress
        logger.info(f"Compressing: {os.path.basename(file)}")
        if os.path.isfile(file):
            with open(file, 'rb') as f:
                raw = f.read()
            cmp = Compressor().compress(raw, Signatures.SC, 1)
            with open(file + ".cmp", 'wb') as out:
                out.write(cmp)

    print(f"Done in {Time(time.time() - start_time)} seconds.")

if __name__ == "__main__":
    main()
