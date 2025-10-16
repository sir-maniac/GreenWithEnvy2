# This file is part of gwe.
#
# Copyright (c) 2020 Roberto Leinardi
#
# gwe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gwe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gwe.  If not, see <http://www.gnu.org/licenses/>.

from dataclasses import dataclass
from pathlib import Path

@dataclass
class SysPaths:
    pkgdata_dir: str
    icon_path: str
    config_path: str

    def get_config_path(self, file: str) -> str:
        return str( Path(self.config_path).joinpath(file) )
