# SC2FLA-FOSS-Edition

SC2FLA-FOSS-Edition is a FOSS tool for converting `.sc` files (Supercell's 2D asset format) into `.fla` (Adobe Animate) files. It allows artists and modders to access and animate Supercell assets freely.

The Original [SC2FLA](https://github.com/sc-workshop/SC) was released by [Daniil](https://github.com/daniil-sv) and [Fred](https://github.com/pavidloq) is now closed-source and has been rewritten in a faster language with more features. 

## Purpose of This Edition

This FOSS edition builds on Daniil's last public SC2FLA version. It adds **basic compatibility with newer SC formats**, particularly for animation preview and file extraction. It **does not** have advanced features from the paid version, but it is a usable solution for those needing basic conversion capabilities.

## Features

- Basic `.sc` to `.fla` conversion
- Downgrade support for SC2 to SC1 format via `ScDowngrade.exe`
- Version detection for `.sc` files
- Support for batch processing of files

## To-do

- Improve logging
- Allow directory argument
- Merge `main.py` and `processor.py`

## Usage

1. Run `setup.py` or manually install pips:

`pip install sc-compression Pillow numpy affine6p colorama lxml ujson`

2. Download the latest release of [ScDowngrade.exe](https://github.com/Daniil-SV/ScDowngrade/releases) and put it in the `~/lib` folder.

3. Put `.sc`, `_dl.sc`, `_tex.sc`, `.sctx` and `_{number}.sc` in the `$assets` folder.

4. Run `run.bat`

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
