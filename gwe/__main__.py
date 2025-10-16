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
import signal
import locale
import gettext
import logging
import sys
from types import TracebackType
from typing import Type
from os.path import abspath, join, dirname

from injector import Injector, inject
from peewee import SqliteDatabase
from reactivex.disposable import CompositeDisposable

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import GLib

from gwe import di
from gwe.conf import APP_PACKAGE_NAME
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


def main(pkgdata_dir: str, icon_path: str) -> int:
    _LOG.debug("main")

    di.PKGDATA_DIR = pkgdata_dir
    di.ICON_PATH = icon_path

    injector = Injector([ProviderModule])

    lifetime = injector.get(GweLifetime)
    application: Application = injector.get(Application)
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, application.quit)
    exit_status = application.run(sys.argv)
    lifetime.cleanup()
    return sys.exit(exit_status)

