#!/usr/bin/env python3

# gwe
#
# Copyright (C) 2016 Roberto Leinardi <roberto@leinardi.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import signal
from pathlib import Path
import sys

source_root = Path(__file__).parent.parent

PKGDATA_DIR = source_root / 'build/meson/data'
ICON_PATH = source_root / 'build/meson/data/icons'
#localedir = source_root / 'build/meson/share/locale'
os.environ['GWE_RUN_LOCAL'] = "1"

sys.path.insert(1, source_root)

signal.signal(signal.SIGINT, signal.SIG_DFL)
# gettext.install('trg', localedir)

if __name__ == '__main__':
    from gwe import __main__
    __main__.main(PKGDATA_DIR.as_posix(), ICON_PATH.as_posix())
