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
from enum import Enum
import time
import logging
from typing import Dict, NewType, Tuple, Any, cast

from gi.repository import Gtk, GLib, Gdk, GObject
from gi.repository.GObject import TYPE_DOUBLE
from injector import singleton, inject

from gwe.conf import GRAPH_COLOR_HEX
from gwe.model.clocks import Clocks
from gwe.presenter.historical_data_presenter import GRAPH_INIT, HistoricalDataViewInterface, HistoricalDataPresenter, MONITORING_INTERVAL, \
    GraphType
from ..model.graph_model import GraphModel
from .widget.graph_view import GraphView
from gwe.repository.nvidia_repository import NvidiaRepository
from gwe.view.graph_stacked_renderer_view import GraphStackedRenderer

_LOG = logging.getLogger(__name__)

GV_MIN_VALUE = 0
GV_MAX_VALUE = 1
GV_CUR_VALUE = 2

HistoricalDataBuilder = NewType('HistoricalDataBuilder', Gtk.Builder)

@singleton
class HistoricalDataView(HistoricalDataViewInterface):
    @inject
    def __init__(self,
                 presenter: HistoricalDataPresenter,
                 builder: HistoricalDataBuilder,
                 nvidia_repository: NvidiaRepository,
                 ) -> None:
        _LOG.debug('init HistoricalDataView')
        self._presenter: HistoricalDataPresenter = presenter
        self._presenter.view = self
        self._builder: Gtk.Builder = builder
        self._builder.connect_signals(self._presenter)
        self._nvidia_repository = nvidia_repository
        self._graphs: Dict[GraphType, Dict[str, Any]] = {}
        self._initial_show = True
        self._init_widgets()

    def _init_widgets(self) -> None:
        self._dialog = cast(Gtk.Dialog, self._builder.get_object('dialog'))
        assert self._dialog is not None
        self._init_graphs()

    def set_transient_for(self, window: Gtk.Window) -> None:
        self._dialog.set_transient_for(window)

    def _init_max_values(self) -> None:
        mem_total, max_clocks = self._nvidia_repository.get_max_values()

        if max_clocks.graphic_max is not None:
            self._graph_models[GraphType.GPU_CLOCK].value_max = max_clocks.graphic_max

        if max_clocks.memory_max is not None:
            self._graph_models[GraphType.MEMORY_CLOCK].value_max = max_clocks.memory_max

        self._graph_models[GraphType.MEMORY_USAGE].value_max = mem_total


    # pylint: disable=attribute-defined-outside-init
    def _init_graphs(self) -> None:
        self._graph_views: Dict[GraphType, Tuple[Gtk.Label, Gtk.Label, Gtk.Label]] = {}
        self._graph_models: Dict[GraphType, GraphModel] = {}

        for graph_type in GraphType:
            self._graph_container = cast(Gtk.Frame, self._builder.get_object(f'graph_container_{graph_type.value}'))
            self._graph_views[graph_type] = (cast(Gtk.Label, self._builder.get_object(f'graph_min_value_{graph_type.value}')),
                                                cast(Gtk.Label, self._builder.get_object(f'graph_max_value_{graph_type.value}')),
                                                cast(Gtk.Label, self._builder.get_object(f'graph_max_axis_{graph_type.value}')))

            max_samples: float = int( MONITORING_INTERVAL / self._presenter.get_refresh_interval() + 1 )
            timespan: int = MONITORING_INTERVAL * 1000 * 1000
            init = GRAPH_INIT[graph_type]

            graph_model = GraphModel(
                column_names=["Col0"],
                max_samples=max_samples,
                timespan=timespan,
                value_min=init.min_value,
                value_max=init.max_value
            )

            self._graph_views[graph_type][GV_MAX_VALUE].set_text(f"{init.max_value:.0f}")
            self._graph_views[graph_type][GV_MIN_VALUE].set_text(f"{init.min_value:.0f}")
            self._graph_views[graph_type][GV_CUR_VALUE].set_text(f"0 {init.unit}")

            graph_model.connect("notify::value-max",
                                type(self)._on_notify_max,
                                self._graph_views[graph_type][GV_MAX_VALUE])
            graph_model.connect("notify::value-min",
                                type(self)._on_notify_min,
                                self._graph_views[graph_type][GV_MIN_VALUE])

            graph_view = GraphView(graph_model)
            graph_renderer = GraphStackedRenderer()
            graph_view.set_hexpand(True)
            graph_view.props.height_request = 80
            graph_renderer.set_line_width(1.5)
            stroke_color = Gdk.RGBA()
            stroke_color.parse(GRAPH_COLOR_HEX)
            stacked_color = Gdk.RGBA()
            stacked_color.parse(GRAPH_COLOR_HEX)
            stacked_color.alpha = 0.5
            graph_renderer.set_stroke_color_rgba(stroke_color)
            graph_renderer.set_stacked_color_rgba(stacked_color)

            graph_view.add_renderer(graph_renderer)

            self._graph_container.add(graph_view)

            graph_model.append(GLib.get_monotonic_time(), 0.0)

            self._graph_models[graph_type] = graph_model

    @staticmethod
    def _on_notify_min(model: GraphModel, _pspec: GObject.ParamSpec, label: Gtk.Label) -> None:
        label.set_text(f"{model.value_min:.0f}")

    @staticmethod
    def _on_notify_max(model: GraphModel, _pspec: GObject.ParamSpec, label: Gtk.Label) -> None:
        label.set_text(f"{model.value_max:.0f}")

    def reset_graphs(self) -> None:
        self._init_graphs()
        self._init_max_values()

    def refresh_graphs(self, data_dict: Dict[GraphType, Tuple[int, float]]) -> None:
        time1 = time.time()
        for graph_type, data in data_dict.items():
            unit = GRAPH_INIT[graph_type].unit
            self._graph_views[graph_type][GV_CUR_VALUE].set_text(f"{data[1]} {unit}")

            model = self._graph_models[graph_type]
            model.append(data[0], data[1])

        time2 = time.time()
        _LOG.debug(f'Refresh graph took {((time2 - time1) * 1000.0):.3f} ms')

    def show(self) -> None:
        if self._initial_show:
            self._initial_show
            self._init_max_values()
        self._dialog.show_all()

    def hide(self) -> None:
        self._dialog.hide()
