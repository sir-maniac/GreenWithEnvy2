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
    is_installed: bool
    """ If program is running in an installed location, rather than in the source tree  """
    has_pkg_resources: bool
    """ If true the resources are in <pkg-dir>/data """
    entry_point_file: Path
    """ Absolute path of the file to run this program """
    pkgdata_dir: Path
    """ Location of the gresource file """
    data_dir: Path
    """ location of various data subdirs (i.e. /usr/share ) """
    icon_path: Path
    """ Path to append to icon search path (i.e. /usr/share/icons ) """
    config_path: Path
    """
        Path of user-level configuration such as:
        - $XDG_CONFIG_HOME/<app_name>
        - $HOME/.config/<app_name>
        - for flatpak: $HOME/.var/app/<app_id>/<app_name>
    """

    def get_config_path(self, file: str) -> str:
        return str( self.config_path.joinpath(file) )
