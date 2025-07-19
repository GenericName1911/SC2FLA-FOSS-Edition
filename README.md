# SC2FLA-FOSS-Edition

SC2FLA-FOSS-Edition is a **Free and Open-source** tool for converting `.sc` files (Supercell's 2D asset format) into `.fla` (Adobe Animate) files.

The Original [SC2FLA](https://github.com/sc-workshop/SC) was released by [Daniil](https://github.com/daniil-sv) and [Fred](https://github.com/pavidloq) is now **closed-source** and has been rewritten by Daniil in a faster language with more features. 

## Features

This FOSS edition builds on Daniil's last public SC2FLA version. It adds **basic compatibility with newer SC formats** and offers **extended support** for SC2FLA. It **does not** have advanced features from the paid version, but it is a usable solution for those needing basic conversion capabilities. It supports:

- Basic `.sc` to `.fla` conversion
- Downgrade support for SC2 to SC1 format via `ScDowngrade.exe`
- Version detection for `.sc` files
- Support for batch processing of files

## Support

This tool is only usable on Windows with no plans to extend OS support. Moreover, I do not plan to implement new sc2fla features, but only to offer extended support.

Feel free to contribute to this project! Any help is greatly appreciated :D

## Usage

1. Run `setup.py` or manually install pips:

`pip install sc-compression Pillow numpy affine6p colorama lxml ujson`

2. Download the latest release of [ScDowngrade.exe](https://github.com/Daniil-SV/ScDowngrade/releases) and put it in the `~/lib` folder.

3. Put `.sc`, `_dl.sc`, `_tex.sc`, `.sctx` and `_{number}.sc` in the `$assets` folder.

4. Run `run.bat`

## To-do

- Improve logging
- Allow directory argument
- Merge `main.py` and `processor.py`

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
