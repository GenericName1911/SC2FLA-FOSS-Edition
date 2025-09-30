# SC2FLA-FOSS-Edition

SC2FLA-FOSS-Edition is a **Free and Open-source** tool for converting `.sc` files (Supercell's 2D asset format) into `.fla` (Adobe Animate) files.

The Original [SC2FLA](https://github.com/sc-workshop/SC) which was released by [Daniil](https://github.com/daniil-sv) and [Fred](https://github.com/pavidloq) is now **closed-source** and has been rewritten by Daniil in a faster language with more features.


## Features

This FOSS edition builds on Daniil's last public SC2FLA version. It adds **basic compatibility with newer SC formats** and offers **extended support** for SC2FLA. It **does not** have advanced features from the paid version, but it is a usable solution for those needing basic conversion capabilities. It supports:

- Basic `.sc` to `.fla` conversion
- Minor Bug fixes
- Version detection for `.sc` files
- Downgrade support for SC2 to SC1 format via `ScDowngrade.exe`
- Decode support for SCTX format via `SctxConverter.exe`
- Support for batch processing of files
- Creating spritesheets via `SCTex.exe` (soon)
- Multithreading for _**way**_  faster conversion (Only bottleneck being CPU) (soon)


## Support

This tool is only usable on Windows with no plans to extend OS support. I'm improving it, but new features are not a priority at all.

For any **_errors_**, feel free to message me anytime on discord `@generic_name_1911` or create an issue. Do _not_ create issues for **feature requests**. 

Feel free to contribute to this project! Any help is greatly appreciated :D

## Dependencies:

1. Python 3.10+ (Added to PATH)
2. pip
3. [ScDowngrade](https://github.com/Daniil-SV/ScDowngrade/releases)
4. [SCTX-Converter](https://github.com/Daniil-SV/SCTX-Converter/releases)
5. [SupercellFlash Texture Tool (Modified by me)](https://github.com/sc-workshop/SupercellFlash)
6. [PVRTexToolCLI](https://docs.imgtec.com/tools-manuals/pvrtextool-manual/html/topics/pvrtextool-cli.html)

## Usage

1. Download the [latest release](https://github.com/GenericName1911/SC2FLA-FOSS-Edition/releases/).

2. Place `.sc`, `_dl.sc`, `_tex.sc`, `.sctx`, and `_{number}.sc` files into the `$assets/` folder.

---

### Installation and Execution

**For V1.x - V3.x**

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Download [ScDowngrade.exe](https://github.com/Daniil-SV/ScDowngrade/releases) and [SctxConverter.exe](https://github.com/Daniil-SV/SCTX-Converter/releases).

3. Place both binaries into the `~\lib` folder.

4. Run `run.bat` or execute via CLI.

**For V4.x+**

1. Install dependencies manually as above, or run:

   ```
   .\user-scripts\setup.py
   ```

   This installs dependencies and downloads the latest release of `ScDowngrade.exe` and `SctxConverter.exe`.

2. Place both binaries into the `~\lib` folder.

3. Run desired scripts from `.\user-scripts` by _dragging them to the main folder and executing_:

   * `setup.py` — Installs dependencies and downloads latest binaries
   * `process folder.bat` — Converts `.sc` files with downgrade support
   * `dump raw.bat` — Dumps RAW resources
   * `spritesheet.bat` — Creates PNG spritesheets [V5.0+]
   * `clean all files.vbs` — Effectively resets the tool

---

### Command-Line Interface (All Versions)

```
usage: main.py [-h] [-p] [-d] [-dx/-cx] [-s] input

Arguments:
  -h, --help             Show this help message and exit  
  -p, --process          Process .sc file or directory  
  -dr, --dump-raw        Dump RAW resources of .sc files [V4+]
  -dp, --dump-png        Dump RAW resources of .sc files [V5+]  
  -dx, --decompress      Decompress .sc files  
  -cx, --compress        Compress .sc files (LZMA | SC | V1)  
  -s, --sort-layers      Enable layer sorting  
```


## Change Log

Interpretation:

```
Not strikethrough = Not implemented  
Not strikethrough w/ next version = In source control, scheduled for next release  
Strikethrough w/ version = Released in that version
PR - User = Pull request by user  
```

* ~~Improve logging [V1.1]~~
* ~~Allow directory as argument [V2.0]~~
* ~~Merge `main.py` and `processor.py` [V2.0]~~
* ~~Fix sc-compression bug [V2.0]~~
* ~~Implement SCTX Converter [V3.0]~~
* ~~Fix bugged textures with SCTX [V3.0]~~
* ~~Set default textfield color to white [V3.0]~~
* ~~Log using Colorama instead of raw ANSI injection [V3.0]~~
* ~~Implement RAW dump feature [V4.0]~~
* ~~Fully rely on SCTX Converter for `.sctx` handling [V4.0] ([PR - 8-bitHacc](https://github.com/GenericName1911/SC2FLA-FOSS-Edition/pull/2))~~
* ~~Separate package for automation/convenience; CLI is still supported for enhanced control [V4.0]~~
* ~~List of dependencies [V5.0]~~
* ~~Fix Khronos textures with PVRTexTool.exe [V5.0]~~
* Implement Spritesheet creation with SCTex.exe
* Downgrade with directory argument (ScD version selector is broken) [Not possible currently]
* Use **Multi-threading**


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
