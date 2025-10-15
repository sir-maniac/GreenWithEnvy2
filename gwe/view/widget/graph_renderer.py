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
# Based on deprecated library 'Dazzle', dzl-graph-renderer copyrighted by
#    Christian Hergert
#

from abc import ABCMeta, abstractmethod
from typing import Optional, override
import typing

import cairo
from gi.repository.Gdk import RGBA
from gi.repository import Gdk
from ...model.graph_model import GraphModel, GraphModelIter

class GraphRenderer(metaclass=ABCMeta):
    @abstractmethod
    def render(self,
               table : GraphModel,
               begin_time : int,
               end_time : int,
               y_begin : int,
               y_end : int,
               cairo_context : cairo.Context,
               area : Gdk.Rectangle) -> None:
        raise NotImplementedError


class GraphLineRenderer(GraphRenderer):
    def __init__(self, stroke_color: Optional[RGBA]=None, line_width: float = 2.0) -> None:
        GraphRenderer.__init__(self)
        self._line_width = line_width
        self._column: int = 0
        self._stroke_color: Optional[RGBA] = stroke_color

    def set_line_width(self, width: float) -> None:
        self._line_width = width
    line_width = property(fset=set_line_width)

    def set_stroke_color(self, stroke_color: str) -> None:
        self._stroke_color = RGBA()
        self._stroke_color.parse(stroke_color)

    def set_stroke_color_rgba(self, stroke_color: RGBA) -> None:
        self._stroke_color = stroke_color

    def get_stroke_color_rgba(self) -> RGBA:
        return self._stroke_color
    stroke_color_rgba = property(get_stroke_color_rgba, set_stroke_color_rgba)

    @override
    def render(self,
               table : GraphModel,
               begin_time : int,
               end_time : int,
               y_begin : int,
               y_end : int,
               cairo_context : cairo.Context,
               area : Gdk.Rectangle) -> None:
        cairo_context.save()

        model_iter: Optional[GraphModelIter] = table.get_iter_first()


        if model_iter is not None:
            model_iter.next()
            max_samples = table.max_samples

            chunk = area.width / float( max_samples - 1 ) / 2.0
            timespan = float(end_time - begin_time)

            last_x = self._calc_x(model_iter, begin_time, timespan, area.width)
            last_y = self._calc_y(model_iter, y_begin, y_end, area.height, self._column)

            cairo_context.move_to(last_x, last_y)

            while model_iter.next():
                x = self._calc_x(model_iter, begin_time, timespan, area.width)
                y = self._calc_y(model_iter, y_begin, y_end, area.height, self._column)

                cairo_context.curve_to(
                    last_x + chunk,
                    last_y,
                    last_x + chunk,
                    y,
                    x,
                    y
                )
                last_x = x
                last_y = y

        cairo_context.set_line_width(self._line_width)

        if self._stroke_color is not None:
            c: RGBA = self._stroke_color
            cairo_context.set_source_rgba(c.red, c.green, c.blue, c.alpha)
        cairo_context.stroke()

        cairo_context.restore()


    @staticmethod
    def _calc_x(model_iter: GraphModelIter, begin: float, timespan: float, width: int) -> float:
        timestamp: int = model_iter.timestamp
        assert timestamp != 0
        return (timestamp - begin) / float(timespan) * width

    @staticmethod
    def _calc_y(model_iter: GraphModelIter,
                range_begin: float,
                range_end: float,
                height: int,
                column: int) -> float:
        y = 0.0
        y = float( model_iter.get_value(column) )

        y -= range_begin
        assert y != 0
        y /= (range_end - range_begin)
        y = height - (y * height)

        return y


