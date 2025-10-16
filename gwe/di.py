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

import logging
import os
from pathlib import Path
import shutil
from typing import NewType
from xdg import BaseDirectory

from gi.repository import Gio, Gtk
from injector import Binder, Module, provider, singleton
from peewee import BooleanField, SqliteDatabase
from playhouse.migrate import SqliteMigrator, migrate
from reactivex.disposable import CompositeDisposable
from reactivex.subject import Subject

from gwe.conf import (APP_DB_NAME, APP_DB_VERSION,
                      APP_EDIT_FAN_PROFILE_UI_NAME,
                      APP_EDIT_OC_PROFILE_UI_NAME, APP_HISTORICAL_DATA_UI_NAME, APP_ID,
                      APP_MAIN_UI_NAME, APP_PACKAGE_NAME,
                      APP_PREFERENCES_UI_NAME)
from gwe.model import fan_profile, overclock_profile, setting, speed_step
from gwe.model.current_fan_profile import CurrentFanProfile
from gwe.model.current_overclock_profile import CurrentOverclockProfile
from gwe.model.fan_profile import FanProfile, FanProfileChangedSubject
from gwe.model.overclock_profile import (OverclockProfile,
                                         OverclockProfileChangedSubject)
from gwe.model.setting import Setting, SettingChangedSubject
from gwe.model.speed_step import SpeedStep, SpeedStepChangedSubject
from gwe.model.sys_paths import SysPaths
from gwe.view.edit_fan_profile_view import EditFanProfileBuilder
from gwe.view.edit_overclock_profile_view import EditOverclockProfileBuilder
from gwe.view.historical_data_view import HistoricalDataBuilder
from gwe.view.main_view import MainBuilder
from gwe.view.preferences_view import PreferencesBuilder

_LOG = logging.getLogger(__name__)

PKGDATA_DIR: str  # set in gwe.__main__
ICON_PATH: str # set in gwe.__main__

_UI_RESOURCE_PATH = "/com/leinardi/gwe/ui/{}"


# pylint: disable=no-self-use
class ProviderModule(Module):
    def configure(self, binder: Binder) -> None:
        config_path = str(Path(BaseDirectory.save_config_path(APP_PACKAGE_NAME)))
        sys_paths = SysPaths(PKGDATA_DIR, ICON_PATH, config_path)

        db = self._create_database(sys_paths.get_config_path(APP_DB_NAME))
        fan_subject = FanProfileChangedSubject(Subject())
        speed_step_subject = SpeedStepChangedSubject(Subject())
        overclock_profile_subject =  OverclockProfileChangedSubject(Subject())
        setting_subject =  SettingChangedSubject(Subject())

        binder.bind(SysPaths, sys_paths)
        binder.bind(SqliteDatabase, to=db)
        binder.bind(FanProfileChangedSubject, fan_subject)
        binder.bind(SpeedStepChangedSubject, speed_step_subject)
        binder.bind(OverclockProfileChangedSubject, overclock_profile_subject)
        binder.bind(SettingChangedSubject, setting_subject)

        # These need to be initialized so builders can find their files.
        # There might be a better place for this, but this seems a better place than the
        #  the top-level `gwe` file.

        resource = Gio.Resource.load(os.path.join(sys_paths.pkgdata_dir, f'{APP_ID}.gresource'))
        resource._register()

        icon_theme: Gtk.IconTheme = Gtk.IconTheme.get_default()
        icon_theme.append_search_path(sys_paths.icon_path)

        # peewee's model fundamentally clashes with injection, requiring
        #  configuration at the class level, rather than at instance
        #  construction. The best compromise I can think of is to set
        #  configuration at injection time.

        CurrentFanProfile._meta.database = db
        CurrentOverclockProfile._meta.database = db
        FanProfile._meta.database = db
        OverclockProfile._meta.database = db
        Setting._meta.database = db
        SpeedStep._meta.database = db

        fan_profile.FAN_PROFILE_CHANGED_SUBJECT = fan_subject
        overclock_profile.OVERCLOCK_PROFILE_CHANGED_SUBJECT = overclock_profile_subject
        setting.SPEED_STEP_CHANGED_SUBJECT = setting_subject
        speed_step.SPEED_STEP_CHANGED_SUBJECT = speed_step_subject


    @singleton
    @provider
    def provide_main_builder(self) -> MainBuilder:
        _LOG.debug("provide Gtk.Builder")
        builder = MainBuilder(Gtk.Builder())
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_resource(_UI_RESOURCE_PATH.format(APP_MAIN_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_edit_fan_profile_builder(self) -> EditFanProfileBuilder:
        _LOG.debug("provide Gtk.Builder")
        builder = EditFanProfileBuilder(Gtk.Builder())
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_resource(_UI_RESOURCE_PATH.format(APP_EDIT_FAN_PROFILE_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_edit_overclock_profile_builder(self) -> EditOverclockProfileBuilder:
        _LOG.debug("provide Gtk.Builder")
        builder = EditOverclockProfileBuilder(Gtk.Builder())
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_resource(_UI_RESOURCE_PATH.format(APP_EDIT_OC_PROFILE_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_historical_data_builder(self) -> HistoricalDataBuilder:
        _LOG.debug("provide Gtk.Builder")
        builder = HistoricalDataBuilder(Gtk.Builder())
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_resource(_UI_RESOURCE_PATH.format(APP_HISTORICAL_DATA_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_preferences_builder(self) -> PreferencesBuilder:
        _LOG.debug("provide Gtk.Builder")
        builder = PreferencesBuilder(Gtk.Builder())
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_resource(_UI_RESOURCE_PATH.format(APP_PREFERENCES_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_thread_pool_scheduler(self) -> CompositeDisposable:
        _LOG.debug("provide CompositeDisposable")
        return CompositeDisposable()

    @staticmethod
    def _create_database(path_to_db: str) -> SqliteDatabase:
        database = SqliteDatabase(path_to_db)

        if os.path.exists(path_to_db):
            if database.pragma('user_version') == 0:
                _LOG.debug("upgrading database to version 1")
                shutil.copyfile(path_to_db, path_to_db + '.bak')

                database.pragma('user_version', 1, permanent=True)

                migrator = SqliteMigrator(database)
                vbios_silent_mode = BooleanField(default=False)
                migrate(
                    migrator.add_column('fan_profile', 'vbios_silent_mode', vbios_silent_mode),
                    migrator.add_column('current_fan_profile', 'vbios_silent_mode', vbios_silent_mode)
                )

                database.commit()
        else:
            database.pragma('user_version', APP_DB_VERSION, permanent=True)

        return database


