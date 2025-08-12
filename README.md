# SC2FLA-FOSS-Edition

SC2FLA-FOSS-Edition is a **Free and Open-source** tool for converting `.sc` files (Supercell's 2D asset format) into `.fla` (Adobe Animate) files.

The Original [SC2FLA](https://github.com/sc-workshop/SC) which was released by [Daniil](https://github.com/daniil-sv) and [Fred](https://github.com/pavidloq) is now **closed-source** and has been rewritten by Daniil in a faster language with more features. 

## Features

This FOSS edition builds on Daniil's last public SC2FLA version. It adds **basic compatibility with newer SC formats** and offers **extended support** for SC2FLA. It **does not** have advanced features from the paid version, but it is a usable solution for those needing basic conversion capabilities. It supports:

- Basic `.sc` to `.fla` conversion
- Minor Bug fixes
- Version detection for `.sc` files
- Downgrade support for SC2 to SC1 format via `ScDowngrade.exe`
- Decode support for .SCTX format via `SctxConverter.exe`
- Support for batch processing of files
- Dump feature for PNG resources

## Support

This tool is only usable on Windows with no plans to extend OS support. I'm slowly improving it, but new features are not a priority at all.

Feel free to contribute to this project! Any help is greatly appreciated :D

## Usage

1. Download the [latest release.](https://github.com/GenericName1911/SC2FLA-FOSS-Edition/releases/)

2. Run `setup.py` or manually install dependencies:
	
	`pip install -r requirements.txt`

3. Download [ScDowngrade.exe](https://github.com/Daniil-SV/ScDowngrade/releases) and [SctxConverter.exe](https://github.com/Daniil-SV/SCTX-Converter/releases).

4 Place both binaries in the `~\lib` folder.

---

### Choose one of the following:

* **Automatic (Quick conversion)**

  1. Place `.sc`, `_dl.sc`, `_tex.sc`, `.sctx`, and `_{number}.sc` files in the `$assets/` folder.
  2. Run `run.bat`
  
* **Command-Line**

```
  usage: main.py [-h] [-p] [-d] [-dx/-cx] [-s] input

  Arguments:
    -h,  --help             Show this help message and exit  
    -p,  --process          Process .sc file or directory  
    -d,  --dump             Dumps .png resources of .sc files (NOT IMPLEMENTED)  
    -dx, --decompress       Decompress .sc files  
    -cx, --compress         Compress .sc files (LZMA | SC | V1)  
    -s,  --sort-layers      Enable layer sorting  
```

## To-do

- ~~Improve logging [V1.1]~~
- ~~Allow directory as argument [V2.0]~~
- ~~Merge `main.py` and `processor.py` [V2.0]~~
- ~~Fix sc-compression bug [V2.0]~~
- ~~Implement SCTX Converter [V3.0]~~
- ~~Fix bugged textures with sctx [V3.0]~~
- ~~Set default textfield colour to white [V3.0]~~
- ~~Log using Colorama instead of raw ANSI code injection [V3.0]~~
- Implement dump feature [V4.0]
- Downgrade with dir arg (ScD supports it, but version selector is broken)
- Separate package for automation/convenience. CLI will still be supported and offers greater control.

## Licensing Notice:

```
Copyright (C) 2025 generic_name_1911

This program is free software: You can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
