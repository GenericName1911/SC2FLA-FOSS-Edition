import sys
import struct
import os
import shutil
import subprocess
import logging

ASSET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "$assets"))  # Asset directory
EXE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "ScDowngrade.exe"))  # Relative path to ScDowngrade.exe

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

def get_used_version(data):
    # Extracts version number from SC binary header.
    if len(data) < 6 or data[:2] != b"SC":
        return None
    big_endian_version = struct.unpack(">I", data[2:6])[0]
    little_endian_version = struct.unpack("<I", data[2:6])[0]
    return little_endian_version if big_endian_version >= 5 else big_endian_version


def downgrade(filepath):
    # Downgrades SC2 files to SC1
    try:
        subprocess.run([
            EXE_PATH,
            filepath,
            filepath,
        ], check=True)
        logger.info(f"Downgraded: {os.path.basename(filepath)}")
    except FileNotFoundError:
        logger.error(f"ScDowngrade.exe not found at path: .\\{EXE_PATH}")
    except subprocess.CalledProcessError:
        logger.error(f"ScDowngrade.exe failed processing: {os.path.basename(filepath)}")
    except Exception as e:
        logger.error(f"Unexpected error during downgrade: {os.path.basename(filepath)} — {e}")

def process_file(filepath):
    """
      - Checks extension
      - Reads version
      - Invokes downgrade if file is SC2 (version >= 5)
    """
    logger.info(f"Processing: {os.path.basename(filepath)}")

    if not filepath.lower().endswith(".sc"):
        logger.warning(f"Invalid file extension: {filepath}")
        return

    with open(filepath, "rb") as f:
        data = f.read()

    version = get_used_version(data)
    if version is None:
        logger.critical(f"Bad File Magic: {os.path.basename(filepath)}")
        return

    if version >= 5:
        logger.info(f"Detected SC2 File!")
        downgrade(filepath)

if __name__ == "__main__":
    # Collect all .sc files under $assets directory and processes them
    sc_files = [os.path.join(ASSET_DIR, f) for f in os.listdir(ASSET_DIR) if f.lower().endswith(".sc")]

    for file_path in sc_files:
        try:
            process_file(file_path)
        except Exception as e:
            logger.error(f"Exception: {e}")
