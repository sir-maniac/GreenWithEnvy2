#!/usr/bin/env python3

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
import os
from pathlib import Path
import signal
import locale
import gettext
import logging
import sys
from types import TracebackType
from typing import NoReturn, Optional, Type
from os.path import abspath, join, dirname

from injector import Injector, inject
from peewee import SqliteDatabase
from reactivex.disposable import CompositeDisposable

import gi

from gwe.model.sys_paths import SysPaths
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import GLib

from gwe import di
from gwe.conf import APP_PACKAGE_NAME, APP_RESOURCE_FILE_NAME, DEFAULT_ICON_PATH, TEST_ICON_PATH
from gwe.model.current_fan_profile import CurrentFanProfile
from gwe.model.current_overclock_profile import CurrentOverclockProfile
from gwe.model.fan_profile import FanProfile
from gwe.model.overclock_profile import OverclockProfile
from gwe.model.setting import Setting
from gwe.model.speed_step import SpeedStep
from gwe.util.log import set_log_level
from gwe.di import ProviderModule
from gwe.app import Application
from gwe.repository.nvidia_repository import NvidiaRepository

WHERE_AM_I = abspath(dirname(__file__))
LOCALE_DIR = join(WHERE_AM_I, 'mo')

signal.signal(signal.SIGINT, signal.SIG_DFL)
# gettext.install('trg', localedir)

set_log_level(logging.INFO)

_LOG = logging.getLogger(__name__)

# POSIX locale settings
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_PACKAGE_NAME, LOCALE_DIR)

gettext.bindtextdomain(APP_PACKAGE_NAME, LOCALE_DIR)
gettext.textdomain(APP_PACKAGE_NAME)

class GweLifetime:
    @inject
    def __init__(self,
                 composite_disposable: CompositeDisposable,
                 nvidia_repository: NvidiaRepository,
                 database: SqliteDatabase) -> None:
        self._composite_disposable = composite_disposable
        self._nvidia_repository = nvidia_repository
        self._database = database
        self._init_database()

        sys.excepthook = self.handle_exception

    def cleanup(self) -> None:
        try:
            _LOG.debug("cleanup")
            self._composite_disposable.dispose()
            self._nvidia_repository.set_all_gpus_fan_to_auto()
            self._database.close()
            # futures.thread._threads_queues.clear()
        except:
            _LOG.exception("Error during cleanup!")


    def handle_exception(self, type_: Type[BaseException], value: BaseException, traceback: TracebackType) -> None:
        if issubclass(type_, KeyboardInterrupt):
            sys.__excepthook__(type_, value, traceback)
            return

        _LOG.critical("Uncaught exception", exc_info=(type_, value, traceback))
        self.cleanup()
        sys.exit(1)


    def _init_database(self) -> None:
        self._database.create_tables([
            SpeedStep,
            FanProfile,
            CurrentFanProfile,
            OverclockProfile,
            CurrentOverclockProfile,
            Setting
        ])

def _get_entry_point() -> str:
    argv0 = sys.argv[0]
    if len(argv0) != 0 and argv0 != '-c':
        return os.path.abspath(sys.argv[0])
    else:
        raise RuntimeError("Could not determine the entry point script")

def _create_sys_paths(pkgdata_dir: str, data_dir: str, icon_path: Optional[str], has_pkg_resources: bool) -> SysPaths:
    assert isinstance(pkgdata_dir, str)

    config_path = Path(GLib.get_user_config_dir()) / APP_PACKAGE_NAME

    is_installed = True

    run_local: bool = 'GWE_RUN_LOCAL' in os.environ
    builddir = os.environ.get('MESON_BUILD_ROOT')
    if run_local:
        is_installed = False
    elif builddir is not None:
        # running in them meson build directory with 'run' or 'debug' target
        is_installed = False
        pkgdata_dir = (Path(builddir)/'data').as_posix()
        data_dir = pkgdata_dir
        icon_path = (Path(builddir)/'data/icons').as_posix()
        os.environ['GSETTINGS_SCHEMA_DIR'] = data_dir

    if icon_path is None:
        icon_path = DEFAULT_ICON_PATH

    return SysPaths(is_installed=is_installed,
                    has_pkg_resources=has_pkg_resources,
                    entry_point_file=Path(_get_entry_point()),
                    pkgdata_dir=Path(pkgdata_dir),
                    data_dir=Path(data_dir),
                    icon_path=Path(icon_path),
                    config_path=config_path)


def main(pkgdata_dir: str,
         data_dir: str,
         icon_path: Optional[str] = None,
         has_pkg_resources: bool=False) -> NoReturn:
    """Main function for this program

    Args:
        pkgdata_dir (str): program specific data directory ( i.e. /usr/share/gwe2 )
        data_dir (str): non-program specific data directory ( i.e. /usr/share )
        icon_path (Optional[str], optional): _description_. Defaults to None.
        has_pkg_resources (bool, optional): _description_. Defaults to False.

    Returns:
        NoReturn: Doesn't return, calls sys.exit()
    """
    _LOG.debug("main")

    sys_paths = _create_sys_paths(pkgdata_dir=pkgdata_dir,
                                  data_dir=data_dir,
                                  icon_path=icon_path,
                                  has_pkg_resources=has_pkg_resources)
    injector = Injector(ProviderModule(sys_paths))

    lifetime = injector.get(GweLifetime)
    application: Application = injector.get(Application)
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, application.quit)
    exit_status = application.run(sys.argv)
    lifetime.cleanup()
    sys.exit(exit_status)

def main_pkg_resources() -> NoReturn:
    """ Main function when resources are installed in <pkg_name>/data """
    pkg_root = Path(__file__).parent
    pkgdata_dir = pkg_root/'data'
    data_dir = pkg_root/'data'
    icon_path = pkg_root/'icons'
    assert pkgdata_dir.is_dir(), f"Could not find resources in '{pkg_root.name}/data'"
    if not icon_path.is_dir():
        icon_path = Path(DEFAULT_ICON_PATH)
    main(pkgdata_dir=pkgdata_dir.as_posix(),
         data_dir=data_dir.as_posix(),
         icon_path=icon_path.as_posix(),
         has_pkg_resources=True)