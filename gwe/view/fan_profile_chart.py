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

from typing import Dict, OrderedDict, cast
import cairo
from gi.repository import Gtk, Gdk, GObject

from gwe.conf import GRAPH_COLOR_HEX

class FanProfileChart(Gtk.DrawingArea):
    """Custom widget for plotting fan speed profiles."""
    __gtype_name__ = "FanProfileChart"

    def __init__(self) -> None:
        super().__init__()
        self._data: Dict[int, int] = {}
        self._hysteresis = 0
        self.set_size_request(400, 300)
        self.connect("draw", self._on_draw)

        self._plot_colour = Gdk.RGBA()
        self._plot_colour.parse(GRAPH_COLOR_HEX)



    def set_data(self, data: Dict[int, int], hysteresis: int = 0) -> None:
        """Set the fan profile data to be plotted."""
        self._data = data
        self._hysteresis = hysteresis
        self.queue_draw()

    def _on_draw(self, widget: Gtk.Widget, cr: cairo.Context) -> None:
        """Handle the drawing of the chart."""

        style = self.get_style_context()

        allocation = self.get_allocation()
        width = allocation.width
        height = allocation.height

        # Clear background
        Gtk.render_background(style, cr, 0, 0, width, height)

        fg_colour: Gdk.RGBA = cast(Gdk.RGBA, style.get_color(Gtk.StateType.NORMAL))

        # Chart margins
        margin_left = 60
        margin_bottom = 40
        margin_top = 20
        margin_right = 20

        chart_width = width - margin_left - margin_right
        chart_height = height - margin_bottom - margin_top

        if chart_width <= 0 or chart_height <= 0:
            return

        vertical_padding = chart_height / 30

        # Draw grid and labels
        self._draw_grid(cr,
                        fg_colour,
                        width,
                        height,
                        chart_width,
                        chart_height,
                        vertical_padding,
                        margin_left,
                        margin_bottom,
                        margin_top,
                        margin_right)

        # Draw data lines
        self._draw_data_lines(cr,
                              width,
                              height,
                              chart_width,
                              chart_height,
                              vertical_padding,
                              margin_left,
                              margin_bottom,
                              margin_top,
                              margin_right)

    def _draw_grid(self,
                   cr: cairo.Context,
                   colour: Gdk.RGBA,
                   width: int,
                   height: int,
                   chart_width: int,
                   chart_height: int,
                   vertical_padding: float,
                   margin_left: int,
                   margin_bottom: int,
                   margin_top: int,
                   margin_right: int) -> None:
        """Draw the grid lines and labels."""

        cr.set_source_rgba(colour.red, colour.green, colour.blue, 0.5)
        cr.set_line_width(0.5)

        # Vertical grid lines (temperature)
        bottom = height - margin_bottom
        h_segment = float(chart_width) / 5

        def temp_line(i: int) -> None:
            x = margin_left + (i * h_segment)
            cr.move_to(x, margin_top)
            cr.line_to(x, bottom)
            cr.stroke()

            # Draw temperature labels
            temp_value = i * 20
            cr.set_font_size(10)
            text = f"{temp_value}°C"
            extents = cr.text_extents(text)
            cr.move_to(x - extents.width / 2, bottom + 15)
            cr.show_text(text)

        # first line solid
        temp_line(0)

        # other lines dashes
        cr.set_dash([1, 0, 0])
        for i in range(1,6):
            temp_line(i)

        # base horizontal line
        cr.set_dash([])
        cr.move_to(margin_left, bottom)
        cr.line_to(width - margin_right, bottom)
        cr.stroke()

        # add a small margin to top and bottom
        inner_height = chart_height - vertical_padding * 2
        inner_bottom = bottom - vertical_padding
        v_segment = inner_height / 5

        cr.set_dash([1, 0, 0])
        # Horizontal grid lines (duty)
        for i in range(6):
            y = inner_bottom - (i * v_segment)
            cr.move_to(margin_left, y)
            cr.line_to(width - margin_right, y)
            cr.set_dash([1, 0, 0])
            cr.stroke()
            cr.set_dash([])

            # Draw duty labels
            duty_value = i * 20
            cr.set_font_size(10)
            text = f"{duty_value}%"
            extents = cr.text_extents(text)
            cr.move_to(margin_left - extents.width - 5, y + extents.height / 2)
            cr.show_text(text)

        # Draw axes
        cr.set_line_width(2)

        # X axis
        cr.move_to(margin_left, height - margin_bottom)
        cr.line_to(width - margin_right, height - margin_bottom)
        cr.stroke()

        # Y axis
        cr.move_to(margin_left, margin_top)
        cr.line_to(margin_left, height - margin_bottom)
        cr.stroke()

        # Draw axis labels
        cr.set_font_size(12)

        # X axis label
        x_label = "Temperature"
        extents = cr.text_extents(x_label)
        cr.move_to(width / 2 - extents.width / 2, height - 5)
        cr.show_text(x_label)

        # Y axis label (rotated)
        y_label = "Duty"
        extents = cr.text_extents(y_label)
        cr.save()
        cr.translate(15, height / 2)
        cr.rotate(-1.5708)  # -90 degrees in radians
        cr.move_to(-extents.width / 2, 0)
        cr.show_text(y_label)
        cr.restore()

    def _draw_data_lines(self,
                         cr: cairo.Context,
                         width: int,
                         height: int,
                         chart_width: int,
                         chart_height: int,
                         vertical_padding: float,
                         margin_left: int,
                         margin_bottom: int,
                         margin_top: int,
                         margin_right: int) -> None:
        """Draw the actual data lines."""
        if not self._data:
            return

        # Sort data by temperature
        sorted_data = OrderedDict(sorted(self._data.items()))

        if len(sorted_data) < 2:
            return

        inner_bottom = height - margin_bottom - vertical_padding
        inner_height = chart_height - vertical_padding * 2

        # Convert data to chart coordinates
        chart_points = []
        for temp, duty in sorted_data.items():
            x = margin_left + (temp / 100) * chart_width
            y = inner_bottom - (duty / 100) * inner_height
            chart_points.append((x, y))

        # Draw main line
        plot_colour = self._plot_colour
        cr.set_source_rgba(plot_colour.red, plot_colour.green, plot_colour.blue, plot_colour.alpha)
        cr.set_line_width(3)
        cr.move_to(chart_points[0][0], chart_points[0][1])

        for point in chart_points:
            cr.line_to(point[0], point[1])

        cr.stroke()

        # Draw points with larger radius
        for point in chart_points:
            cr.arc(point[0], point[1], 5, 0, 2 * 3.14159)
            cr.fill()

        # Draw hysteresis line if hysteresis > 0
        if self._hysteresis > 0:
            hysteresis_points = []
            for temp, duty in sorted_data.items():
                temp_with_hysteresis = temp - self._hysteresis
                if temp_with_hysteresis >= 0:  # Only draw if temperature is valid
                    x = margin_left + (temp_with_hysteresis / 100) * chart_width
                    y = inner_bottom - (duty / 100) * inner_height
                    hysteresis_points.append((x, y))

            if len(hysteresis_points) >= 2:
                # Draw hysteresis line (dashed)
                cr.set_line_width(1)
                cr.set_dash([5, 5])  # Dashed line
                cr.move_to(hysteresis_points[0][0], hysteresis_points[0][1])

                for point in hysteresis_points:
                    cr.line_to(point[0], point[1])

                cr.stroke()
                cr.set_dash([])  # Reset dash