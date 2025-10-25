# This file is part of gwe.
#
# Copyright (c) 2018 Roberto Leinardi
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
from pathlib import Path
from typing import Optional

from gi.repository import GLib
from injector import inject

from gwe.conf import DESKTOP_ENTRY, APP_ICON_NAME, APP_DESKTOP_ENTRY_NAME, APP_PACKAGE_NAME
from gwe.model.sys_paths import SysPaths
from gwe.util.desktop.desktop_parser import DesktopParser

DESKTOP_ENTRY_EXEC = 'Exec'
DESKTOP_ENTRY_ICON = 'Icon'
AUTOSTART_FLAG = 'X-GNOME-Autostart-enabled'

class DesktopEntry():
    @inject
    def __init__(self,
                 sys_paths: SysPaths):
        self._sys_paths = sys_paths
        self.autostart_file_path = Path(GLib.get_user_config_dir()).joinpath('autostart').joinpath(APP_DESKTOP_ENTRY_NAME)
        self.application_entry_file_path = Path(GLib.get_user_data_dir()).joinpath('applications').joinpath(APP_DESKTOP_ENTRY_NAME)

    def set_autostart_entry(self, is_enabled: bool) -> None:
        desktop_parser = DesktopParser(str(self.autostart_file_path))

        if not self.autostart_file_path.is_file():
            for key, value in DESKTOP_ENTRY.items():
                desktop_parser.set(key, value)

            desktop_parser.set(DESKTOP_ENTRY_ICON, APP_ICON_NAME)

        desktop_parser.set(DESKTOP_ENTRY_EXEC, f'{self._sys_paths.bin_file} --hide-window --delay')
        desktop_parser.set(AUTOSTART_FLAG, str(is_enabled).lower())
        desktop_parser.write()


    def add_application_entry(self) -> None:
        desktop_parser = DesktopParser(str(self.application_entry_file_path))

        for k, v in DESKTOP_ENTRY.items():
            desktop_parser.set(k, v)

        desktop_parser.set(DESKTOP_ENTRY_ICON, APP_ICON_NAME)
        desktop_parser.set(DESKTOP_ENTRY_EXEC, self._sys_paths.bin_file)
        desktop_parser.write()
