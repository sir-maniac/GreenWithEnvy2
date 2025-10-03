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
#
# Code based on GNOME Usage from Petr Štětka
#

from typing import Optional, override
import cairo

from gi.repository import GObject, Gdk

from gwe.graph.graph_model import GraphModel, GraphModelIter
from gwe.graph.graph_renderer import GraphRenderer


class GraphStackedRenderer(GraphRenderer):

    def __init__(self) -> None:
        GraphRenderer.__init__(self)
        self._column = 0
        self._line_width = 1.0
        self._stroke_color_rgba: Gdk.RGBA = Gdk.RGBA(0.5, 0.5, 0.5, 1)
        self._stacked_color_rgba: Gdk.RGBA = Gdk.RGBA(0.5, 0.5, 0.5, 0.5)

    def set_stroke_color_rgba(self, color: Gdk.RGBA) -> None:
        self._stroke_color_rgba = color

    def set_stacked_color_rgba(self, color: Gdk.RGBA) -> None:
        self._stacked_color_rgba = color

    def set_line_width(self, width: float) -> None:
        self._line_width = width

    @override
    def render(self,
                  table: GraphModel,
                  begin_time: int,
                  end_time: int,
                  y_begin: float,
                  y_end: float,
                  cairo_context: cairo.Context,
                  area: Gdk.Rectangle) -> None:
        cairo_context.save()

        timespan = float(end_time - begin_time)
        model_iter: Optional[GraphModelIter] = table.get_iter_first()
        if model_iter is not None:
            model_iter.next()
            chunk = area.width / (table.max_samples - 1) / 2.0
            last_x = self._calc_x(model_iter, begin_time, timespan, area.width)
            last_y = float(area.height)

            cairo_context.move_to(last_x, last_y)

            while model_iter.next():
                x = self._calc_x(model_iter, begin_time, timespan, area.width)
                y = self._calc_y(model_iter, y_begin, y_end, area.height, self._column)

                cairo_context.curve_to(last_x + chunk, last_y, last_x + chunk, y, x, y)

                last_x = x
                last_y = y

        # save path for stroke color
        stroke_path = cairo_context.copy_path()

        # background
        cairo_context.set_line_width(self._line_width)
        cairo_context.set_source_rgba(self._stacked_color_rgba.red,
                                      self._stacked_color_rgba.green,
                                      self._stacked_color_rgba.blue,
                                      self._stacked_color_rgba.alpha)
        cairo_context.rel_line_to(0, area.height)
        cairo_context.stroke_preserve()
        cairo_context.close_path()
        cairo_context.fill()

        # foreground line
        cairo_context.append_path(stroke_path)
        cairo_context.set_source_rgba(self._stroke_color_rgba.red,
                                      self._stroke_color_rgba.green,
                                      self._stroke_color_rgba.blue,
                                      self._stacked_color_rgba.alpha)
        cairo_context.stroke()
        cairo_context.restore()

    @staticmethod
    def _calc_x(model_iter: GraphModelIter, begin: int, timespan: float, width: int) -> float:
        timestamp: int = model_iter.timestamp
        return (timestamp - begin) / timespan * width

    @staticmethod
    def _calc_y(model_iter: GraphModelIter,
                range_begin: float,
                range_end: float,
                height: int,
                column: int) -> float:
        y = 0.0
        y = float( model_iter.get_value(column) )

        y -= range_begin
        y /= (range_end - range_begin)
        y = height - (y * height)

        return y
