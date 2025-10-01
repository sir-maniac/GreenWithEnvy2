# This file is part of gwe.
#
# Copyright (c) 2025 Ryan Bloomfield
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
#
# Based on deprecated library 'Dazzle', dzl-graph-view copyrighted by
#    Christian Hergert
#

from hmac import new
from typing import Any, List, Optional
import cairo
from gi.repository import GObject, Gdk, Gtk, GLib
from gi.repository.GLib import SOURCE_CONTINUE, SOURCE_REMOVE
from .graph_model import GraphModel
from .graph_renderer import GraphRenderer


class GraphView(Gtk.DrawingArea):
    table: GObject.Property

    def __init__(self, table: GraphModel, **props: Any) -> None:
        super().__init__(**props)
        self._model: GraphModel = table
        self._surface_dirty: bool = True
        self._tick_handler: int = 0
        self._renderers: List[GraphRenderer] = []
        self._missed_count: int = 0
        self._surface: Optional[cairo.Surface] = None
        self._x_offset: float = 0.0

        # Connect signals
        table.connect("notify::value-max", type(self)._on_notify_value_min_max, self)
        table.connect("notify::value-min", type(self)._on_notify_value_min_max, self)
        table.connect("notify::timespan", type(self)._on_notify_timespan, self)
        table.connect("changed", type(self)._on_model_changed, self)

        self.connect("draw", type(self)._on_draw)
        self.connect("size-allocate", type(self)._on_size_allocate)
        self.connect("destroy", type(self)._on_destroy)

        self.queue_allocate()

    def _clear_surface(self) -> None:
        self._surface_dirty = True

    def get_model(self) -> Optional[GraphModel]:
        return self._model

    table = GObject.Property(getter=get_model)

    def set_css_name(self, name: str) -> None:
        # Set the CSS name for styling, if desired
        self.get_style_context().add_class(name)

    def add_renderer(self, renderer: GraphRenderer) -> None:
        self._renderers.append(renderer)
        self._clear_surface()

    @staticmethod
    def _on_model_changed(_model: GraphModel, self: "GraphView") -> None:
        self._x_offset = 0
        self._clear_surface()

    @staticmethod
    def _on_notify_value_min_max(_obj: GObject.Object,
                                 _pspec: GObject.ParamSpec,
                                 self: "GraphView") -> None:
        self.queue_allocate()

    @staticmethod
    def _on_notify_timespan(_obj: GObject.Object,
                            _pspec: GObject.ParamSpec,
                            self: "GraphView") -> None:
        if self.get_visible() and self.get_child_visible():
            self.queue_draw()

    def _on_size_allocate(self, allocation: Gdk.Rectangle) -> None:
        old_alloc = self.get_allocation()

        if allocation.width != old_alloc.width or allocation.height != old_alloc.height:
            self._surface = None  # Will be recreated on next draw
            self._clear_surface()

    def _on_draw(self, cr: cairo.Context) -> bool:
        self._missed_count = 0
        alloc = self.get_allocation()
        self._ensure_surface()
        # Draw background (optional, for styling)
        style_context: Gtk.StyleContext = self.get_style_context()
        style_context.save()
        style_context.add_class("view")
        Gtk.render_background(style_context, cr, 0, 0, alloc.width, alloc.height)
        style_context.restore()
        # Draw the graph surface
        cr.save()
        if self._surface:
            cr.set_source_surface(self._surface, self._x_offset * alloc.width, 0)
            cr.rectangle(0, 0, alloc.width, alloc.height)
            cr.fill()
        cr.restore()
        return Gdk.EVENT_PROPAGATE

    def _on_destroy(self) -> None:
        if self._tick_handler != 0:
            self.remove_tick_callback(self._tick_handler)
            self._tick_handler = 0
        self._surface = None

    def _ensure_surface(self) -> None:
        alloc = self.get_allocation()
        if self._surface is None:
            self._surface_dirty = True
            window = self.get_window()
            assert window is not None
            self._surface = window.create_similar_surface(
                cairo.CONTENT_COLOR_ALPHA,
                alloc.width,
                alloc.height)
        if self._model is None:
            return
        if self._surface_dirty:
            self._surface_dirty = False
            cr = cairo.Context(self._surface)
            cr.save()
            cr.rectangle(0, 0, alloc.width, alloc.height)
            cr.set_operator(cairo.OPERATOR_CLEAR)
            cr.fill()
            cr.restore()

            y_begin: int = int( self._model.value_min )
            y_end: int = int ( self._model.value_max )
            end_time = self._model.get_end_time()
            begin_time: int = end_time - self._model.timespan
            for renderer in self._renderers:
                cr.save()
                renderer.render(self._model,
                                begin_time,
                                end_time,
                                y_begin,
                                y_end,
                                cr,
                                alloc)
                cr.restore()
        if self._tick_handler == 0:
            self._tick_handler = self.add_tick_callback(self._tick_cb, None)


    @staticmethod
    def _tick_cb(view: "GraphView",
                 frame_clock: Gdk.FrameClock,
                 user_data: Any) -> bool:

        def remove_handler() -> None:
            if view._tick_handler != 0:
                view.remove_tick_callback(view._tick_handler)
                view._tick_handler = 0

        if view._surface is None or view._model is None or not view.get_visible():
            remove_handler()
            return SOURCE_REMOVE

        # If we've missed drawings for the last 10 tick callbacks, chances are we're
        # visible, but not being displayed to the user because we're not top-most.
        # Disable ourselves in that case too so that we don't spin the frame-clock.
        #
        # We'll be re-enabled when the next ensure_surface() is called (upon a real
        # draw by the system).
        #
        # The missed_count is reset on draw().
        if view._missed_count > 10:
            remove_handler()
            return SOURCE_REMOVE
        else:
            view._missed_count = view._missed_count + 1

        timespan = float( view._model.timespan )
        if timespan == 0:
            remove_handler()
            return SOURCE_REMOVE

        alloc = view.get_allocation()

        frame_time = GLib.get_monotonic_time()
        end_time = view._model.get_end_time()

        x_offset = -((frame_time - end_time) / timespan)
        if x_offset != view._x_offset:
            view._x_offset = x_offset
            view.queue_draw()

        return SOURCE_CONTINUE
